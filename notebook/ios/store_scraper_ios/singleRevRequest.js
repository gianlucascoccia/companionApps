var ios = require('app-store-scraper');
const app = require('app-store-scraper/lib/app');
const { Console } = require('console');
var fs = require('fs')

var appId = process.argv[2].trim();
var page =  process.argv[3];
var input = {
              id: appId,
              sort: ios.sort.HELPFUL,
              page: page
            };

ios.reviews(input).then(function(apps){
  if(apps.length != 0){
        fs.appendFile("data/raw/reviews/" + appId + ".json", JSON.stringify(apps), (err)=>{
        if(err) {
            console.log(err)
            process.exit(1)
        }
         else {
          console.log(JSON.stringify(apps.length))
          process.exit()
         } 
      })
    }
    }).catch(function(e){
      console.log('There was an error fetching the reviews!');
      console.log(e.message);
      process.exit(1)
    });