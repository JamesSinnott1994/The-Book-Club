$(document).ready(function(){
    // Sidenav
    $('.sidenav').sidenav();

    // Resize event, for making paragraph text the same height
    // (Keeps CTA buttons at the one level)
    // https://www.techiedelight.com/trigger-window-resize-event-javascript/
    $(window).trigger('resize');
    $(window).resize(makeParagraphHeightSame);

    // Make height of CTA (Call-To-Action) paragraphs the same
    function makeParagraphHeightSame() {
        let maxHeight = 0;

        $(".call-to-action-area p").each((i, p) => {
            if ($(p).height() > maxHeight) { 
                maxHeight = $(p).height();
            }
        });

        $(".call-to-action-area p").height(maxHeight);
    }

    // Genre select
    $('select').formSelect();

    // Make each book div the same height on the books page
    function makeBookDivHeightSame() {
        let maxHeight = 0;

        $("#book-display-area .book").each((i, book) => {
            if ($(book).height() > maxHeight) { 
                maxHeight = $(book).height();
            }
        });

        $("#book-display-area .book").height(maxHeight);
    }
    makeBookDivHeightSame();

    // Expandable search icon
    $(".fa-search").click(function(){
        $(".searchbar").toggleClass("active");
        $(".icon").toggleClass("active");
        $("input[type='text']").toggleClass("active");
    });

    // Star ratings
    // https://codepen.io/mcallaro88/pen/EWQdRX?html-preprocessor=pug

    // Gets the span width of the filled-ratings span
    // this will be the same for each rating
    var star_rating_width = $('.fill-ratings span').width();
    // Sets the container of the ratings to span width
    // thus the percentages in mobile will never be wrong
    $('.star-ratings').width(star_rating_width);

    // Add click event to star span elements on add review form
    $(`.empty-ratings-review input[type="radio"]`).each((i, star) => {

        $(star).bind('click', () => {

            let starNoClicked = parseInt(star.id.substring(star.id.indexOf('-') + 1));
            console.log(starNoClicked);
            console.log(star);

            $(".empty-ratings-review span").each((i, span) => {
                let currentStar = i+1;

                if (currentStar <= starNoClicked) {
                    console.log("ZZZZZZZZ")
                    $(span).css('color', '#e7711b');
                } else {
                    $(span).css('color', '#ccc');
                }
            })

         });

    });

    // Modal
    $('.modal').modal();

    $(".review-edit-delete .delete-btn").each((i, review) => {
        $(review).bind('click', () => {

            // console.log(review);
            // console.log(review.id);

            let href = $("#delete-review").attr("href");
            console.log(href);

            let newHref = `?review_id=${review.id}`;

            // console.log(newHref);
            // console.log(href+newHref);

            let combinedHref = href+newHref;
            console.log(combinedHref);

            $("#delete-review").attr("href", combinedHref);

            // book_id = $("#book-id").attr("class");
            // console.log(book_id);

            // $("#review-modal .modal-footer").append(`
            //     <a id="delete-review" href="{{ url_for('delete_review', book_id=${book_id}, review_id=${review.id}) }}" class="modal-close waves-effect waves-green btn-flat">Yes</a>
            //     <a href="#" class="modal-close waves-effect waves-green btn-flat">No</a>
            // `);

         });
    });

});