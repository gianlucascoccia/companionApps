var store = require('google-play-scraper');

function print_results(data) {
	console.log(JSON.stringify(data));
}

function print_error(message) {
	console.log(JSON.stringify(message));
}

store.app({appId: process.argv[2]}).then(print_results).catch(print_error);