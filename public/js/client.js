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
            // TODO Get tags and update card
            t.board('id').then((board) => {
              t.card('id', 'name').then((card) => {
                var params = $.param({
                  token: token,
                  board: board.id,
                  card: card.id,
                  text: card.name
                });
                $.ajax({
                  url: `/predict?` + params,
                  type: 'GET',
                  success: function() {
                    console.log('Success');
                  },
                  error: function(err) {
                    console.error('Error deleting from server: ' + JSON.stringify(err));
                  }
                });
              });
            })
          }
        }
      }];
    });
  }
});