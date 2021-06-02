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

    // // Change active class when a Pagination link is clicked on
    // // Binds click events to the pagination list items on the books page
    // let numberOfPages = 0;
    // $(".pagination .pag-link").each((i, link) => {
    //     $(link).bind('click', () => {
    //         $(link).addClass("pag-active");
    //     });
    // });
});