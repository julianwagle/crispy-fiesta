const url = document.location.toString().toLowerCase();
const http = url.split('//')[0];
const path = url.split('//')[1];
const domain = path.split('/')[0];
const page_title_one = path.split('/')[1];
const page_title_two = path.split('/')[2];