#!/usr/bin/env node

const bulkIndex = require('./bulk-index');

/**
 * yargsを利用したコマンド群
 * ref. https://github.com/yargs/yargs
 */
require('yargs')
  .scriptName('search-engine')
  .usage('$0 <cmd> [args]')
  /**
   * インデックスを実行するためのコマンド
   */
  .command(
    // コマンド
    'index',
    // 説明
    '文書データを読み込みインデックスを行う',
    // 引数オプション
    (yargs) => {
      yargs.positional('inputFilePath', {
        type: 'string',
        describe: '文書データのファイルパス'
      });
      yargs.positional('storagePath', {
        type: 'string',
        describe: 'ストレージのファイルパス(.sqliteファイルを想定)'
      });
      yargs.positional('count', {
        type: 'number',
        default: 1000,
        describe: 'インデックスする文書数'
      });
      yargs.positional('parallel', {
        type: 'number',
        default: 4,
        describe: 'flush時の並行処理数'
      });
    },
    // 処理
    (args) => {
      bulkIndex();
    }
  )
  .help().argv;
