module.exports = {
    chainWebpack: config => {
      config.module
        .rule('js')
        .test(/\.js$/)
        .include
        .add(/node_modules\/chart\.js/)  // Chart.js をトランスパイル対象に含める
        .end()
        .use('babel-loader')
        .loader('babel-loader')
        .tap(options => {
          return {
            presets: ['@babel/preset-env']
          };
        });
    }
  };
  