const webpack = require('webpack');

const config = require('./webpack.config.dev');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');

module.exports = Object.assign({}, config, {
  plugins: config.plugins.concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify('production'),
      },
    }),
  ]),
  optimization: {
    minimizer: [
      new UglifyJsPlugin({
        uglifyOptions: {
          compress: {
            ie8: false,
          },
          mangle: {
            ie8: false,
          },
          output: {
            comments: false,
            ie8: false,
          },
        },
      }),
    ],
  }
});
