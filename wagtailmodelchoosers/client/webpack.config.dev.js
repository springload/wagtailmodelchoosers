const path = require('path');
const webpack = require('webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const outputPath = path.join(__dirname, '..', 'static', 'wagtailmodelchoosers');

module.exports = {
  entry: {
    wagtailmodelchoosers: './wagtailmodelchoosers/client/wagtailmodelchoosers.js',
    draftailmodelchoosers: './wagtailmodelchoosers/client/draftailmodelchoosers.js',
    polyfills: './wagtailmodelchoosers/client/polyfills.js',
  },
  output: {
    path: outputPath,
    filename: '[name].js',
  },
  plugins: [
    new webpack.NoEmitOnErrorsPlugin(),
    new MiniCssExtractPlugin(),
  ],
  module: {
    rules: [
      {
        test: /\.js$/,
        use: ['babel-loader'],
        exclude: /node_modules/,
      },
      {
        test: /\.css$/i,
        use: [MiniCssExtractPlugin.loader, 'css-loader'],
      },
    ],
  },
};
