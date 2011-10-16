// Baseado no exemplo disponivel em http://code.google.com/apis/analytics/docs/gdata/2.0/gdataJavascript.html

// Load the Google data JavaScript client library.
google.load('gdata', '2.x', {packages: ['analytics']});

// Set the callback function when the library is ready.
google.setOnLoadCallback(init);

/**
 * This is called once the Google Data JavaScript library has been loaded.
 * It creates a new AnalyticsService object, adds a click handler to the
 * authentication button and updates the button text depending on the status.
 */
function init() {
  myService = new google.gdata.analytics.AnalyticsService('InterCon 2011');
  scope = 'https://www.google.com/analytics/feeds';
  var button = document.getElementById('authButton');

  // Add a click handler to the Authentication button.
  button.onclick = function() {
    // Test if the user is not authenticated.
    if (!google.accounts.user.checkLogin(scope)) {
      // Authenticate the user.
      google.accounts.user.login(scope);
    } else {
      // Log the user out.
      google.accounts.user.logout();
      getStatus();
    }
  }
  getStatus();
}

/**
 * Utility method to display the user controls if the user is 
 * logged in. If user is logged in, get Account data and
 * get Report Data buttons are displayed.
 */
function getStatus() {
  var getAccountButton = document.getElementById('getAccount');
  getAccountButton.onclick = getAccountFeed;
  
  var getDataButton = document.getElementById('getData');
  getDataButton.onclick = getDataFeed;

  var dataControls = document.getElementById('dataControls');
  var loginButton = document.getElementById('authButton');
  if (!google.accounts.user.checkLogin(scope)) {
    dataControls.style.display = 'none';   // hide control div
    loginButton.innerHTML = 'Login';
    document.getElementById('authButton').className = "btn success";
  } else {
    dataControls.style.display = 'block';  // show control div
    loginButton.innerHTML = 'Logout';
    document.getElementById('authButton').className = "btn danger";
  }
}

/**
 * Main method to get account data from the API.
 */
function getAccountFeed() {
  var myFeedUri =
      'https://www.google.com/analytics/feeds/accounts/default?max-results=50';
  myService.getAccountFeed(myFeedUri, handleAccountFeed, handleError);
}

/**
 * Handle the account data returned by the Export API by constructing the inner parts
 * of an HTML table and inserting into the HTML file.
 * @param {object} result Parameter passed back from the feed handler.
 */
function handleAccountFeed(result) {
  // An array of analytics feed entries.
  var entries = result.feed.getEntries();

  // Create an HTML Table using an array of elements.
  var outputTable = ['<table><tr>',
                     '<th>Account Name</th>',
                     '<th>Profile Name</th>',
                     '<th>Profile ID</th>',
                     '<th>Table Id</th></tr>'];

  // Iterate through the feed entries and add the data as table rows.
  for (var i = 0, entry; entry = entries[i]; ++i) {

    // Add a row in the HTML Table array for each value.
    var row = [
      entry.getPropertyValue('ga:AccountName'),
      entry.getTitle().getText(),
      entry.getPropertyValue('ga:ProfileId'),
      entry.getTableId().getValue()
    ].join('</td><td>');
    outputTable.push('<tr><td>', row, '</td></tr>');
  }
  outputTable.push('</table>');

  // Insert the table into the UI.
  document.getElementById('outputDiv').innerHTML =
      outputTable.join('');
}

/**
 * Main method to get report data from the Export API.
 */
function getDataFeed() {
var myFeedUri = 'https://www.google.com/analytics/feeds/data' +
    '?start-date=2011-06-01' +
    '&end-date=2011-10-01' +
    '&dimensions=ga:keyword' +
    '&metrics=ga:visits' +
    '&sort=-ga:visits' +
    '&filters=ga:keyword!%3D(not%20set)' +
    '&max-results=50' +
    '&ids=' + document.getElementById('tableId').value;
  
  myService.getDataFeed(myFeedUri, handleDataFeed, handleError);
}

/**
 * Handle the data returned by the Export API by constructing the 
 * inner parts of an HTML table and inserting into the HTML File.
 * @param {object} result Parameter passed back from the feed handler.
 */
function handleDataFeed(result) {
 
 // An array of Analytics feed entries.
 var entries = result.feed.getEntries();
 
 // Create an HTML list using an array of elements.
 var outputTable = ['<ul id="keywordcloud">'];

  // Iterate through the feed entries and add the data as list items.
  for (var i = 0, entry; entry = entries[i]; ++i) {
     outputTable.push('<li value="', entry.getValueOf('ga:visits'), '" title="', entry.getValueOf('ga:keyword'), '">', entry.getValueOf('ga:keyword'), '</li>');
   }
   outputTable.push('</ul>');

  // Insert the table into the UI.
  document.getElementById('outputDiv').innerHTML =
      outputTable.join('');
  
  // Generate tag cloud.
  $("#keywordcloud").tagcloud({type:"sphere",sizemin:8,sizemax:44,power:.3,colormin:"69c",colormax:"c06",height:500});
}

/**
 * Alert any errors that come from the API request.
 * @param {object} e The error object returned by the Analytics API.
 */
function handleError(e) {
  var error = 'There was an error!\n';
  if (e.cause) {
    error += e.cause.status;
  } else {
    error.message;
  }
  alert(error);
}
