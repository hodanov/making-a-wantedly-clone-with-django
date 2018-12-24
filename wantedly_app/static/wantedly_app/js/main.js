// ------------------------
// --- Initial settings　---
// ------------------------
$(document).ready(function() {
  Promise.all([])
  .then(fontAwesomeFix)
  .then(fadeOutEffect)
  .then(featuredSlider)
  .then(tooltip)
  .then(DomOperationInProfileEditPage)
  // .then(ajaxForPosting)
  .then(ajaxPostProfileEditData)
})

// ------------------------
// --- FontAwesome fix ---
// ------------------------
function fontAwesomeFix() {
  (function() {
    $(document).on("turbolinks:load", function() {
      return FontAwesome.dom.i2svg()
    })
  }).call(this)
}

// ------------------------
// ---　Fade-out effect　---
// ------------------------
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

// ------------------------
// ---　Slider　---
// ------------------------
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

function tooltip() {
  $('[data-toggle="tooltip"]').tooltip()
}

// ------------------------
// --- Profile edit ---
// ------------------------
function DomOperationInProfileEditPage() {
  var editableData = $('.editable-data')
  var formForEditing = $('.form-for-editing')
  var btnForEditing = $('.btn-for-editing')
  var btnToCancelEditing = $('.btn-to-cancel-editing')
  var formForAdding = $('.form-for-adding')
  var btnForAdding = $('.btn-for-adding')
  var btnToCancelAdding = $('.btn-to-cancel-adding')
  var btnToSubmit = $('.post-form-to-edit-profile .post-button-for-profile-edit')
  var btnToUploadPortfolioImage = $('.upload-portfolio-image-btn')
  var inputFormToUploadPortfolioImage = $('.upload-portfolio-image')
  var portfolioImageGroup = $('.portfolio-image-group')

  for (var i = 0; i < editableData.length; i++) {
    toggleDataToForm(i)
    cancelEditing(i)
  }
  for (var j = 0; j < formForAdding.length; j++) {
    toggleAddingForm(j)
    cancelAdding(j)
  }
  charCounter()
  for (var k = 0; k < btnToUploadPortfolioImage.length; k++) {
    uploadPortfolioImage(k)
    readUploadedPortfolioImage(k)
  }

  function toggleDataToForm(i) {
    $(btnForEditing[i]).on('click', function(){
      if ($(this).hasClass('btn-for-adding') == false) {
        // Process when pressing "Edit button".
        $(editableData[i]).toggle()
        $(formForEditing[i]).toggle()
      }
    })
    // Process when pressing editable data.
    $(editableData[i]).on('click', function(){
      $(editableData[i]).toggle()
      $(formForEditing[i]).toggle()
    })
    // Process when pressing submit button.
    $(btnToSubmit[i]).on('click', function(){
      $(editableData[i]).toggle()
      $(formForEditing[i]).toggle()
    })
  }

  function cancelEditing(i) {
    // Process when pressing "cancel button".
    $(btnToCancelEditing[i]).on('click', function(){
      $(editableData[i]).toggle()
      $(formForEditing[i]).toggle()
    })
  }

  function toggleAddingForm(j) {
    $(btnForAdding[j]).on('click', function() {
      // Process when pressing "Add button".
      $(formForAdding[j]).toggle()
    })
  }

  function cancelAdding(j) {
    // Process when pressing "cancel button".
    $(btnToCancelAdding[j]).on('click', function(){
      $(formForAdding[j]).toggle()
    })
  }

  function charCounter() {
    // Display the remaining number of characters that can be entered.
    var textarea = $('.form-for-editing textarea')
    var counter = $('.char-counter span')
    var maxLength = []
    for (var i = 0; i < textarea.length; i++) {
      maxLength[i] = $(counter[i]).text()
      updateCount(i, maxLength[i])
    }
    function updateCount(i, maxLength) {
      var cs = $(textarea[i]).val().length;
      var count = maxLength - cs
      $(counter[i]).text(count);
      $(textarea[i]).on('input', function() {
        cs = $(this).val().length;
        count = maxLength - cs
        $(counter[i]).text(count);
      })
    }
  }

  function uploadPortfolioImage(k) {
    $(btnToUploadPortfolioImage[k]).on('click', function() {
      $(this).next(inputFormToUploadPortfolioImage[k]).click()
    })
  }

  function readUploadedPortfolioImage(k) {
    $(inputFormToUploadPortfolioImage[k]).on('change', function(){
      if (this.files && this.files[0]) {
        var reader = new FileReader()
        reader.onload = function (e) {
          $(portfolioImageGroup[k]).append(`
            <div class="form-group col-md-3">
              <div class="responsive-img-wrapper portfolio-image">
                <div class="responsive-img" style="background-image: url(${e.target.result})">
                </div>
              </div>
            </div>`)
        }
        reader.readAsDataURL(this.files[0])
      }
    })
  }
}

// ------------------------
// --- Ajax for posting ---
// ------------------------
function ajaxPostProfileEditData() {
  $('.post-form-to-edit-profile').on('submit', function(e){
    e.preventDefault()
    var dataString = $(this).serialize()
    ajaxPostData(dataString)
  })

  $('.post-button-to-edit-privacy-level').on('click', function(e){
    e.preventDefault()
    var form = $(this).closest('form')
    var dataString = $(form).serialize()
    if ($(this).attr('value')) {
      var nameAttr = $(this).attr('name')
      var valAttr = $(this).attr('value')
    }
    dataString = `${dataString}&${nameAttr}=${valAttr}`
    ajaxPostData(dataString)
  })

  function ajaxPostData(dataString) {
    $.ajax({
      url : "post/", // the endpoint
      type : "POST",
      data : dataString, // data sent with the post request
      success : function(json) {// handle a successful response
        console.log(json)
        console.log("success") // sanity check
        replaceTarget = json.target_instance_name
        if (json.changing_privacy_level) {
          $(`#${replaceTarget}-privacy-level`).html(json.icon)
        }
        else {
          switch (replaceTarget) {
            case "profile":
              $('#profile-editable-data #favorite-words').html(`
                <i class="fas fa-quote-left"></i>
                ${json.favorite_words}
                <i class="fas fa-quote-right"></i>
              `)
              $('#profile-editable-data #job').html(`<i class="fas fa-briefcase"></i>${json.job}`)
              $('#profile-editable-data #location').html(`<i class="fas fa-map-marker-alt"></i>${json.location}`)
              $('#profile-edit-modal').modal('hide')
              break
            case "introduction":
              $('#introduction-editable-data').html(`<p>${json.introduction.replace(/\n/g, '<br>')}</p>`)
              break
            case "statement":
              $('#statement-editable-data').html(`<p>${json.statement.replace(/\n/g, '<br>')}</p>`)
              break
            case "work-history":
              $(`#${json.uuid} .experience-organization`).html(`<span>${json.organization}<span class="editable-mark"><i class="fas fa-pen"></i>編集する</span></span>`)
              $(`#${json.uuid} .experience-job`).text(json.job)
              $(`#${json.uuid} .experience-date`).text(`${json.from_date.slice(0, json.from_date.length-3)} - ${json.to_date.slice(0, json.to_date.length-3)}`)
              $(`#${json.uuid} .experience-description`).text(json.experience)
              break
            case "portfolio":
              $(`#${json.uuid} .profile-portfolio-title`).html(`<span>${json.title}<span class="editable-mark"><i class="fas fa-pen"></i>編集する</span></span>`)
              $(`#${json.uuid} .profile-portfolio-date`).text(`${json.made_at.slice(0, json.made_at.length-3)}`)
              $(`#${json.uuid} .profile-portfolio-link`).text(`${json.url}`)
              $(`#${json.uuid} .profile-portfolio-detail`).text(`${json.detail}`)
              break
            case "related-link":
              $(`#${json.uuid} .profile-related-link-title`).html(`<span>${json.url}<span class="editable-mark"><i class="fas fa-pen"></i>編集する</span></span>`)
              break
            case "educational-bg":
              $(`#${json.uuid} .education-school`).html(`<span>${json.school}<span class="editable-mark"><i class="fas fa-pen"></i>編集する</span></span>`)
              $(`#${json.uuid} .education-major`).text(`${json.major}`)
              $(`#${json.uuid} .education-graduated-at`).text(`${json.graduated_at.slice(0, json.graduated_at.length-3)}`)
              $(`#${json.uuid} .education-detail`).text(`${json.detail}`)
              break
          }
        }
      },
      error : function(xhr,errmsg,err) {// handle a non-successful response
        $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
        " <a href='#' class='close'>&times;</a></div>") // add the error to the dom
        console.log(xhr.status + ": " + xhr.responseText) // provide a bit more info about the error to the console
      }
    })
  }
}
