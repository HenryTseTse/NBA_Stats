function checkOtherShowing() {
    let array = ['#scoring-leaders', '#rebounding-leaders', '#assisting-leaders', '#stealing-leaders', '#blocking-leaders'];
    for (let i = 0; i < array.length; i++) {
        let $target = $(`${array[i]}`);
        if ($target.is(':visible')) {
            $target.hide();
        }
    }
}

function toggleScoringLeaders() {
    let $target = $('#scoring-leaders');
    checkOtherShowing();
    if ($target.is(':visible')) {
        $target.fadeOut(200);
    } else {
        $target.fadeIn(333);
    }
}

function toggleReboundingLeaders() {
    let $target = $('#rebounding-leaders');
    checkOtherShowing();
    if ($target.is(':visible')) {
        $target.fadeOut(200);
    } else {
        $target.fadeIn(333);
    }
}

function toggleAssistingLeaders() {
    let $target = $('#assisting-leaders');
    checkOtherShowing();
    if ($target.is(':visible')) {
        $target.fadeOut(200);
    } else {
        $target.fadeIn(333);
    }
}

function toggleStealingLeaders() {
    let $target = $('#stealing-leaders');
    checkOtherShowing();
    if ($target.is(':visible')) {
        $target.fadeOut(200);
    } else {
        $target.fadeIn(333);
    }
}

function toggleBlockingLeaders() {
    let $target = $('#blocking-leaders');
    checkOtherShowing();
    if ($target.is(':visible')) {
        $target.fadeOut(200);
    } else {
        $target.fadeIn(333);
    }
}

$('#scoring-leader-dropdown').on("click", toggleScoringLeaders);
$('#rebounding-leader-dropdown').on("click", toggleReboundingLeaders);
$('#assisting-leader-dropdown').on("click", toggleAssistingLeaders);
$('#stealing-leader-dropdown').on("click", toggleStealingLeaders);
$('#blocking-leader-dropdown').on("click", toggleBlockingLeaders);