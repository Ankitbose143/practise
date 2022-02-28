const mssqlExport = require('mssql-to-csv');

// All config options supported by https://www.npmjs.com/package/mssql
let dbconfig = {
      user: 'starboy',
      password: 'Just24373!',
      server: 'dataserver.gramener.com',
      database: 'starboy',
      requestTimeout: 32000000,
      pool: {
            max: 30,
            min: 12,
            idleTimeoutMillis: 300000
      }
};
let tables = ["REF_PRODUCT", "REF_PRODUCT_MEDIA",
      "FACT_MEDIA_ANALYSIS", "FACT_MEDIA", "FACT_MARKET_PERF_AGG_WK",
      "FACT_MARKET_PERF_AGG_MTH", "FACT_MARKET_PEN_AGG_MTH", "DIM_COUNTRY"];
let options = {
      ignoreList: [], // tables to ignore
      tables: [],                  // empty to export all the tables
      outputDirectory: 'csv',
      log: true,
      header: false                // true to export column names as csv header
};

mssqlExport(dbconfig, options).then(function () {
      console.log("All done successfully!");
      process.exit(0);
}).catch(function (err) {
      console.log(err.toString());
      process.exit(-1);
});