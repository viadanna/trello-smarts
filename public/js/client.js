/* global TrelloPowerUp */
/* global $ */

// we can access Bluebird Promises as follows
var Promise = TrelloPowerUp.Promise;

// We need to call initialize to get all of our capability handles set up and registered with Trello
TrelloPowerUp.initialize({
  'card-buttons': function(t, opts) {
    // check that viewing member has write permissions on this board
    if (opts.context.permissions.board !== 'write') {
      return [];
    }
    return t.get('member', 'private', 'token')
    .then(function(token){
      return [{
        icon: 'https://cdn.hyperdev.com/07656aca-9ccd-4ad1-823c-dbd039f7fccc%2Fzzz-grey.svg',
        text: 'Autotag',
        callback: function(context) {
          if (!token) {
            // Load authorization
            context.popup({
              title: 'Authorize Your Account',
              url: './auth.html',
              height: 75
            });
          } else {
            // Send card id to backend
            t.card('id').then((card) => {
              var params = $.param({
                token: token
              });
              $.ajax({
                url: `/predict/${card.id}?${params}`,
                type: 'GET',
                success: function() {
                  console.log('Success');
                },
                error: function(err) {
                  console.error('Error predicting: ' + JSON.stringify(err));
                }
              });
            });
          }
        }
      }];
    });
  }
});