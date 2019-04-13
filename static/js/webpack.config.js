const path = require('path');

const ExtractTextPlugin = require('extract-text-webpack-plugin');

// Create extract plugin for each file you want to create in resulting bundle
const extractStyles = new ExtractTextPlugin('../../css/dist/wb.css');


module.exports = {
  entry: {
    index: './src/index.js',
  },
  mode: 'production',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js'
  },
  module: {
     rules: [
      // ...
      {
        test: /\.less$/,
        use: extractStyles.extract({
          fallback: 'style-loader',
          use: [
            { loader: 'css-loader', options: { importLoaders: 1 } }, // importLoaders equals to number of loaders in array after this one.
            'less-loader'
          ]
        })
      },
      {
        test: /\.scss$/,
        use: extractStyles.extract({
          fallback: 'style-loader',
          use: [
            { loader: 'css-loader', options: { importLoaders: 1, url: false } }, // importLoaders equals to number of loaders in array after this one.
            'sass-loader'
          ]
        })
      },
       {
        test: /\.css$/,
        use: extractStyles.extract({
          fallback: 'style-loader',
          use: 'css-loader'
        })
      }
    ]

  },
  plugins: [
      extractStyles
  ]
};