var store = require('app-store-scraper');

function print_results(data) {
	console.log(JSON.stringify(data));
}

function print_error(message) {
	console.log(JSON.stringify(message));
}

store.app({id: process.argv[2]}).then(print_results).catch(print_error);
