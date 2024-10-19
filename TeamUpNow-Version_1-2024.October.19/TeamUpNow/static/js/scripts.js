
  // Helper function to determine if all values are zero
  function areAllValuesZero(values) {
    return values.every(value => value === 0);
  }


        // New variables for posts count and favorites count
        var postsCount = {{ posts_count }};  // Assuming posts_count is a variable in your context
        var favoritesCount = {{ posts_favorites_count }};  // Assuming posts_favorites_count is a variable in your context
      
        // Initialize the second pie chart for posts count and favorites count
        var ctx2 = document.getElementById('favoritesPieChart').getContext('2d');
        var postFavoriteData = [postsCount, favoritesCount];
        
        var favoritesPieChart = new Chart(ctx2, {
          type: 'doughnut',
          data: {
            labels: [`Teaching: ${postsCount}`, `Learning: ${favoritesCount}`],  // Labels for the new chart
            datasets: [{
              data: postFavoriteData,  // Data for the new chart
              backgroundColor: areAllValuesZero(postFavoriteData) ? [
                'transparent',  // Transparent if zero
                'transparent'
              ] : [
                'rgba(75, 192, 75, 0.2)',  // Light green
                'rgba(153, 102, 255, 0.2)'  // Light purple
              ],
              borderColor: [
                'rgba(75, 192, 75, 1)',    // Dark green
                'rgba(153, 102, 255, 1)'   // Dark purple
              ],  
              borderWidth: 1,
              hoverOffset: 4
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,  // Allows resizing based on the canvas size
            cutout: '95%',  // Makes the doughnut chart "thin"
            plugins: {
              legend: {
                display: true,  // Show legend with labels
              },
              tooltip: {
                callbacks: {
                  label: function(tooltipItem) {
                    return tooltipItem.label;  // Show the custom labels in tooltips
                  }
                }
              }
            }
          }
        });



  // New variables for following count and followers count
  var followingCount = {{ following_count }};  // Assuming following_count is a variable in your context
  var followersCount = {{ followers_count }};  // Assuming followers_count is a variable in your context

  // Initialize the third pie chart for following count and followers count
  var ctx3 = document.getElementById('followersPieChart').getContext('2d');
  var followingFollowersData = [followingCount, followersCount];

  var followersPieChart = new Chart(ctx3, {
    type: 'doughnut',
    data: {
      labels: [`Mentees: ${followersCount}`, `Mentors: ${followingCount}`],  // Labels for the new chart
      datasets: [{
        data: followingFollowersData,  // Data for the new chart
        backgroundColor: areAllValuesZero(followingFollowersData) ? [
          'transparent',  // Transparent if zero
          'transparent'
        ] : [
          'rgba(75, 192, 75, 0.2)',  // Light green
          'rgba(153, 102, 255, 0.2)'  // Light purple
        ],
        borderColor: [
          'rgba(75, 192, 75, 1)',    // Dark green
          'rgba(153, 102, 255, 1)'   // Dark purple
        ],
        borderWidth: 1,
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,  // Allows resizing based on the canvas size
      cutout: '95%',  // Makes the doughnut chart "thin"
      plugins: {
        legend: {
          display: true,  // Show legend with labels
        },
        tooltip: {
          callbacks: {
            label: function(tooltipItem) {
              return tooltipItem.label;  // Show the custom labels in tooltips
            }
          }
        }
      }
    }
  });
  