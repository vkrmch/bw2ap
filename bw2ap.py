import argparse
import os
from gpm import config, logging, os as gpmos
import csv
import pandas as pd
import numpy as np

cfg = config.Config(script=__file__, create=True)
cfg.read()

log = logging.Log(script=__file__, log_level=cfg.LOG_LEVEL, tsformat='YYYYMMDDHHMISS')

def do(source_file):
    if os.path.exists(source_file):
        log.info('reading source file: {}'.format(source_file))
        df = pd.read_csv(source_file, dtype=str)

        required_columns = [
            'name',
            'login_uri',
            'login_username',
            'login_password',
            'fields',
            'notes',
            'login_totp'
        ]
        # Check required columns
        for column in required_columns:
            if column not in df.columns:
                log.error('file does not contain required columns')
                log.error('columns found: {}'.format(df.columns.tolist()))
                log.error('columns required: {}'.format(required_columns))
                return 1

        log.info('source row_count: {}'.format(df.shape[0]))

        # fill null values with ""
        df.fillna(value='', inplace=True)

        # combine fields and notes with a pipe '|'
        df['fields_notes'] = (np.where(df['notes'] != '', df['notes'], '') +
                              np.where(np.logical_and(df['fields'] != '', df['notes'] != ''), '|', '') +
                              np.where(df['fields'] != '', 'Custom Fields: ' + df['fields'], ''))

        # select only title, login_url, login_username, login_password, fields, notes, login_totp
        df = df[['name', 'login_uri', 'login_username', 'login_password', 'fields_notes', 'login_totp']]

        # rename fields
        df = df.rename(
            columns={
                'name': 'Title',
                'login_uri': 'URL',
                'login_username': 'Username',
                'login_password': 'Password',
                'fields_notes': 'Notes',
                'login_totp': 'OTPAuth',
            }
        )

        # convert multiple urls into rows
        df['URL'] = df['URL'].str.split(',')
        df = df.explode('URL')

        target_folder = gpmos.get_parent_folder(source_file)
        target_file = os.path.join(target_folder, gpmos.get_filename_wo_extension(source_file) + '_converted.csv')
        log.info('target file: {}'.format(target_file))
        log.info('target row_count: {}'.format(df.shape[0]))
        df.to_csv(target_file, index=False, quoting=csv.QUOTE_ALL, encoding='utf-8')
    else:
        log.error('file {} does not exist'.format(source_file))
        return 1
    return 0

if __name__ == "__main__":
    log.info('begin')
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='full path of the source filename')
    args = parser.parse_args()

    do(source_file=args.source)
    log.info('end')
