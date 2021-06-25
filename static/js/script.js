/*jshint esversion: 6 */
/*globals $:false */
$(document).ready(function(){
    $('.sidenav').sidenav();

    // Resize event, for making paragraph text the same height
    // (Keeps Call-to-action buttons at the one level)
    // https://www.techiedelight.com/trigger-window-resize-event-javascript/
    $(window).trigger('resize');
    $(window).resize(makeParagraphHeightSame);

    // Genre select
    $('select').formSelect();

    // Expandable search icon
    $(".fa-search").click(function(){
        $(".searchbar").toggleClass("active");
        $(".icon").toggleClass("active");
        $("input[type='text']").toggleClass("active");
    });

    makeBookDivHeightSame();
    fillStars();
    bindStarClickEvents();
    bindDeleteBtnClickEvents();

    // Opens modal with trigger
    $('.modal').modal();
});

function makeParagraphHeightSame() {
    /*
    Make height of CTA (Call-To-Action) paragraphs the same
    */
    let maxHeight = 0;

    $(".call-to-action-area p").each((i, p) => {
        if ($(p).height() > maxHeight) { 
            maxHeight = $(p).height();
        }
    });

    $(".call-to-action-area p").height(maxHeight);
}

function makeBookDivHeightSame() {
    /*
    Make each book div the same height on the books page
    */
    let maxHeight = 0;

    $(".books-display-area .book").each((i, book) => {
        if ($(book).height() > maxHeight) { 
            maxHeight = $(book).height();
        }
    });

    $(".books-display-area .book").height(maxHeight);
}

function fillStars() {
    /*
    Star ratings
    https://codepen.io/mcallaro88/pen/EWQdRX?html-preprocessor=pug

    Gets the span width of the filled-ratings span,
    this will be the same for each rating

    Sets the container of the ratings to span width
    thus the percentages in mobile will never be wrong
    */
    var star_rating_width = $('.fill-ratings span').width();
    $('.star-ratings').width(star_rating_width);
}

function bindStarClickEvents() {
    /*
    Adds click event to the star radio buttons on the add review form
    */
    $(`.empty-ratings-review input[type="radio"]`).each((i, star) => {

        $(star).bind('click', () => {

            // Gets star number
            let starNoClicked = parseInt(star.id.substring(star.id.indexOf('-') + 1));

            // Fills up the stars with a golden colour based
            // on the star number clicked
            $(".empty-ratings-review span").each((i, span) => {
                let currentStar = i+1;

                if (currentStar <= starNoClicked) {
                    $(span).css('color', '#e7711b');
                } else {
                    $(span).css('color', '#ccc');
                }
            });

        });

    });
}

function bindDeleteBtnClickEvents() {
    /*
    For each delete button on the Book page we bind a click event

    This event triggers an anonymous function, which creates
    a new href attribute based on the "review_id" of the review to
    be deleted

    This is then added to the "delete-review" id for the "Yes"
    button in the modal window
    */
    $(".review-edit-delete .delete-btn").each((i, review) => {
        $(review).bind('click', () => {

            // Gets href off of "Yes" button in modal window
            // i.e. {{ url_for('delete_review', book_id=book._id) }}
            // i.e. /delete_review/60b4ce2f61f366b649e89519
            let oldHref = $("#delete-review").attr("href");

            // Gets id of review to be deleted
            // .ie ?review_id=60d0c56af773271d99833a63
            let reviewQueryString = `?review_id=${review.id}`;

            // Combines the two
            let newHref = oldHref+reviewQueryString;

            // Creates a new URL for the "Yes" button
            $("#delete-review").attr("href", newHref);

         });
    });
}