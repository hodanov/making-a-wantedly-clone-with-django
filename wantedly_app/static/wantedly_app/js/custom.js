(function() {
  $(document).on("turbolinks:load", function() {
    return FontAwesome.dom.i2svg()
  })
}).call(this)

$(document).ready(function() {
  Promise.all([])
  .then(fadeOutEffect)
  .then(featuredSlider)
})

// ---Fade-out effect---
function fadeOutEffect() {
  $(window).scroll(function() {
    var scrolled = $(window).scrollTop()
    var backgroundContainer = '.background2 > .responsive-img'
    $('.hero').each(function(index, element) {
      // var initY = $(this).offset().top
      var initY = 0
      var height = $(this).height()
      var width = $(this).width()
      var endY  = initY + $(this).height()

      // Check if the element is in the viewport.
      var visible = isInViewport(this)
      if(visible) {
        var diff = scrolled - initY
        var ratio = (1 - (diff / height) * 1.5)
        $(backgroundContainer).css('opacity', ratio)
      }
    })
  })
  function isInViewport(node) {
    var rect = node.getBoundingClientRect()
    return (
      (rect.height > 0 || rect.width > 0) &&
      rect.bottom >= 0 &&
      rect.right >= 0 &&
      rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.left <= (window.innerWidth || document.documentElement.clientWidth)
    )
  }
}

// ---Slider---
function featuredSlider() {
  if ($('.slide-window')) {
    var slideWrapper = $('.slide-wrapper')
    var slideNum = $('.slide').length - 1
    var maxSlideNum = $('.slide').length - 1
    var slideWidth = $('.slide-window').outerWidth()
    var slideSetWidth = slideWidth * slideNum
    var prevBtn = '.slide-control-left'
    var nextBtn = '.slide-control-right'
    var direction
    var clickFlg = true

    var rotationInterval = setInterval(function(){
      moveSlide(direction = 'right')
    }, 10000)

    $(window).bind("focus", resetInterval()).bind("blur", function() {
    // $(window).bind("focus").bind("blur", function() {
      clearInterval(rotationInterval)
    })

    $(prevBtn).on('click', function(){
      if (clickFlg) {
        clickFlg = false
        startProcess(direction = 'left')
      }
    })
    $(nextBtn).on('click', function(){
      if (clickFlg) {
        clickFlg = false
        startProcess(direction = 'right')
      }
    })

    function startProcess(direction) {
      resetInterval()
      rotateArrow(direction)
      moveSlide(direction)
    }
    function moveSlideTimer() {
      moveSlide(direction = 'right')
    }
    function resetInterval() {
      clearInterval(rotationInterval)
      rotationInterval = setInterval(function(){
        moveSlide(direction = 'right')
      }, 10000)
    }
    function rotateArrow(direction) {
      var slideCtlLine1 = '.slide-control-' + direction + ' .slide-control-line:nth-child(1)'
      var slideCtlLine2 = '.slide-control-' + direction + ' .slide-control-line:nth-child(2)'
      $(slideCtlLine1).removeClass('rotate-' + direction + '-top')
      $(slideCtlLine2).removeClass('rotate-' + direction + '-down')
      $(slideCtlLine1).outerWidth()
      $(slideCtlLine2).outerWidth()
      $(slideCtlLine1).addClass('rotate-' + direction + '-top')
      $(slideCtlLine2).addClass('rotate-' + direction + '-down')
    }
    function moveSlide(direction) {
      slideWrapper.addClass('transition')
      if (direction === 'left') {
        slideWrapper.css('transform', 'translateX(' + -slideWidth + 'px)')
        $('.slide:last').clone().prependTo(slideWrapper)
        slideWrapper.css('left', 0).one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',
        function(e) {
          $('.slide:last').remove()
          slideWrapper.removeClass('transition')
          slideWrapper.css({'left': - slideWidth, 'transform': ''})
          clickFlg = true
        })
      }
      else if (direction === 'right') {
        $('.slide:first').clone().appendTo(slideWrapper)
        slideWrapper.css('left', 2 * -slideWidth).one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',
        function(e) {
          $('.slide:first').remove()
          slideWrapper.removeClass('transition')
          slideWrapper.css('left', - slideWidth)
          clickFlg = true
        })
      }
    }
  }
}
