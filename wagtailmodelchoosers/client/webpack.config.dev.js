const path = require('path');
const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

const outputPath = path.join(__dirname, '..', 'static', 'wagtailmodelchoosers');

module.exports = {
  entry: {
    wagtailmodelchoosers: './wagtailmodelchoosers/client/wagtailmodelchoosers.js',
    polyfills: './wagtailmodelchoosers/client/polyfills.js',
  },
  output: {
    path: outputPath,
    filename: '[name].js',
  },
  plugins: [
    new webpack.NoEmitOnErrorsPlugin(),
    new ExtractTextPlugin('wagtailmodelchoosers.css'),
  ],
  module: {
    rules: [
      {
        test: /\.js$/,
        use: ['babel-loader'],
        exclude: /node_modules/,
      },
      {
        test: /\.css$/,
        use: ExtractTextPlugin.extract({
          use: ['css-loader'],
        }),
      },
    ],
  },
};
