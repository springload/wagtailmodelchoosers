const path = require("path");
const webpack = require("webpack");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

const outputPath = path.join(__dirname, "..", "static", "wagtailmodelchoosers");

module.exports = {
  entry: {
    wagtailmodelchoosers:
      "./wagtailmodelchoosers/client/wagtailmodelchoosers.tsx",
    draftailmodelchoosers:
      "./wagtailmodelchoosers/client/draftailmodelchoosers.tsx",
    polyfills: "./wagtailmodelchoosers/client/polyfills.js",
  },
  output: {
    path: outputPath,
    filename: "[name].js",
  },

  devtool: "source-map",

  resolve: {
    extensions: [".tsx", ".ts", ".js"],
  },

  plugins: [new webpack.NoEmitOnErrorsPlugin(), new MiniCssExtractPlugin()],
  module: {
    rules: [
      { test: /\.tsx?$/, loader: "ts-loader" },
      {
        test: /\.js$/,
        use: ["babel-loader"],
        exclude: /node_modules/,
      },
      {
        test: /\.css$/i,
        use: [MiniCssExtractPlugin.loader, "css-loader"],
      },
    ],
  },
};
