$(document).ready(function() {
    // Function to update project container with HTML
    function updateProjects(response) {
        console.log(response.html);
        $('.projects-container').html(
            response.html
        );
    }

    // Function to fetch search results
    function fetchSearchResults(searchQuery) {
        var searchUrl = $('.search-container').data('search-url');
        $.ajax({
            url: searchUrl,
            type: 'GET',
            data: {
                'search': searchQuery
            },
            success: function(response) {
                updateProjects(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    }

    // Perform search as user types
     $(document).on('input', '.search-bar', function() {
        let searchQuery = $(this).val().trim();
        if (searchQuery.length > 0) {
            fetchSearchResults(searchQuery);
        } else {
            // Clear search results if input is empty
            updateProjects({html: ''});
        }
    });
});