$(document).ready(function(){
    $('#rating_success .close').click(function(){
        $('#rating_success').hide();
    });
    $('#rating_error .close').click(function(){
        $('#rating_error').hide();
    });

    var stars = $('.rating-stars li.star');
    for (i = 0; i < current_rating; i++) {
        $(stars[i]).addClass('selected');
    }  
  
    $('#stars li').on('mouseover', function(){
      var onStar = parseInt($(this).data('value'), 10);
     
      $(this).parent().children('li.star').each(function(e){
        if (e < onStar) {
          $(this).addClass('hover');
        }
        else {
          $(this).removeClass('hover');
        }
      });
      
    }).on('mouseout', function(){
      $(this).parent().children('li.star').each(function(e){
        $(this).removeClass('hover');
      });
    });
    
    
    $('#stars li').on('click', function(){
      var onStar = parseInt($(this).data('value'), 10);
      var stars = $(this).parent().children('li.star');
      for (i = 0; i < stars.length; i++) {
        $(stars[i]).removeClass('selected');
      }
      
      for (i = 0; i < onStar; i++) {
        $(stars[i]).addClass('selected');
      }

      var ratingValue = parseInt($('#stars li.selected').last().data('value'), 10);
      $.ajax({
          method: 'POST',
          url: rating_ajax_url,
          data: {rating: ratingValue, csrfmiddlewaretoken: csrf_token},
          success: function(response){
            if(response.message == 'success'){
                $('#average_rating').html(response.average_rating);
                $('#latest_ratings').html('');
                for(var rating of response.ratings){
                    $('#latest_ratings').append(`<div class="card shadow-sm p-2 d-inline-block col-12 text-center">
                                                    <h5>`+ rating.rating +`<i class='inline-star fa fa-star fa-fw'></i>
                                                    <span class="text-secondary"> by `+ rating.user +`</span>
                                                    </h5>
                                                </div>`);
                }

                $('#rating_success').show();
            } else {
                $('#rating_error').show();
            }

          },
          error: function(response){
            $('#rating_error').show();
          }
      });
      
    });
  });