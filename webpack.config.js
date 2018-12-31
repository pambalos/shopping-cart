const path = require('path');
const webpack = require('webpack');

module.exports = {
  mode: 'development',

  entry: {
    index: './js/index.js'
  },
  output: {
    path: path.resolve(__dirname, 'static/lib'),
    filename: '[name].js',
    publicPath: '/static/lib'
  },
  devtool: 'source-map',
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'style-loader',
          loader: 'css-loader',
          loader: 'babel-loader',
          query: {
            cacheDirectory: true,
            presets: ['es2015', 'react', 'stage-0', 'env'],
          }
        }
      },
      {
        test: /\.css$/,
        include: /node_modules/,
        loaders: ['style-loader', 'css-loader'],
      },
    ]
  }
};
