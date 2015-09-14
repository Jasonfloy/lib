var path = require("path");
module.exports = {
  entry: {
        app: "./app.coffee",
  	},
  output: {
  		path: path.join(__dirname, "build"),
  		filename: "[name].bundle.js",
  		chunkFilename: "[id].chunk.js"
  	},
  module: {
    loaders: [
      { test: /\.coffee$/, loader: "coffee-loader" },
      { test: /\.less$/, loader: "style!css!less" },
      { test: /\.(html|tpl)$/, loader: "html" },
      { test: /\.css$/, loader: "style!css" },
    ]
  },
  resolve: {
    extensions: ["", ".web.coffee", ".web.js", ".coffee", ".js"]
  },
  externals: {
    vue: "vue",
    jquery: "jquery",
    underscore: "underscore",
    director:'director',
    simditor:"simditor"
  }
}
