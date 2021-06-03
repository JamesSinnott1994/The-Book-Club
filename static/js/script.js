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
        console.log("HERE");
    }
    makeBookDivHeightSame();
});