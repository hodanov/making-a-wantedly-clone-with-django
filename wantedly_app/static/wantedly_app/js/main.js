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
  // -------------------------
  // Process about "Edit form".
  // -------------------------
  // Process when pressing "editable data".
  $(document).on('click', '.editable-data', function(){
    $(this).toggle()
    $(this).next('.form-for-editing').toggle()
  })
  // Process when pressing "Edit button".
  $(document).on('click', '.btn-for-editing', function(){
    if ($(this).hasClass('btn-for-adding') == false) {
      $(this).closest('.profile-config').next('.editable-data').toggle()
      $(this).closest('.profile-config').next().next('.form-for-editing').toggle()
    }
  })
  // Process when pressing "submit or cancel button".
  $(document).on('click', '.post-button-for-profile-edit, .btn-to-cancel-editing', function(){
    $(this).closest('.form-for-editing').toggle()
    $(this).closest('.form-for-editing').prev('.editable-data').toggle()
  })
  // Process when pressing "delete button".
  $(document).on('click', '.delete-btn', function() {
    var dataInstanceType = $(this).attr('data-instance-type')
    var dataInstanceId = $(this).attr('data-instance-id')
    $('#delete-profile-modal input[name="target-instance-name"]').attr('value', dataInstanceType)
    $('#delete-profile-modal input[name="delete-target-instance-id"]').attr('value', dataInstanceId)
  })

  // -------------------------
  // Process about "Add form".
  // -------------------------
  var formForAdding = $('.form-for-adding')
  var btnForAdding = $('.btn-for-adding')
  var btnToCancelAdding = $('.btn-to-cancel-adding')
  var submitAdd = $('.post-button-for-profile-add')
  for (var j = 0; j < formForAdding.length; j++) {
    toggleAddingForm(j)
    cancelAdding(j)
  }
  function toggleAddingForm(j) {
    // Process when pressing "Add button".
    $(btnForAdding[j]).on('click', function() {
      $(formForAdding[j]).toggle()
    })
    // Process when pressing "submit button".
    $(submitAdd[j]).on('click', function() {
      $(formForAdding[j]).toggle()
    })
  }
  function cancelAdding(j) {
    // Process when pressing "cancel button".
    $(btnToCancelAdding[j]).on('click', function(){
      $(formForAdding[j]).toggle()
    })
  }

  // -------------------------
  // Display the remaining number of characters that can be entered.
  // -------------------------
  $(document).on('input', '.form-for-editing textarea', function() {
    calculateNumber(this)
  })
  $(document).on('input', '.form-for-adding textarea', function() {
    calculateNumber(this)
  })
  function calculateNumber(tmpThis) {
    var counter = $(tmpThis).next('.char-counter').children('span')
    var maxLength = $(tmpThis).next('.char-counter').attr('data-max-length')
    var cs = $(tmpThis).val().length
    var count = maxLength - cs
    counter.text(count)
  }

  // -------------------------
  // Upload an image when pressing "upload btn".
  // -------------------------
  $(document).on('click', '.upload-portfolio-image-btn', function() {
    var inputToUploadPortfolioImage = $(this).next('.upload-portfolio-image')
    var portfolioImageGroup = inputToUploadPortfolioImage.closest('.form-row').next().next('.portfolio-image-group')

    inputToUploadPortfolioImage.click()
    inputToUploadPortfolioImage.off('change').on('change', function(e) {
      if (e.target.files && e.target.files[0]) {
        var files = e.target.files
        for (var i = 0; i < files.length; i++) {
          var file = files[i]
          var reader = new FileReader()
          reader.onload = function (e) {
            portfolioImageGroup.append(`
              <div class="form-group col-md-3">
                <div class="responsive-img-wrapper portfolio-image">
                  <div class="responsive-img" style="background-image: url(${e.target.result})">
                  </div>
                </div>
              </div>`)
          }
          reader.readAsDataURL(file)
        }
      }
    })
  })
}

// ------------------------
// --- Ajax for posting ---
// ------------------------
function ajaxPostProfileEditData() {
  $('.post-form-to-edit-profile, .post-form-to-add-profile, .post-form-to-delete-profile').on('submit', function(e){
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

  $('.post-form-to-edit-image, .post-form-to-add-portfolio, .post-form-to-edit-portfolio').on('submit', function(e){
    e.preventDefault()
    var dataFile = new FormData(this)
    ajaxPostUploadedFile(dataFile)
  })

  function ajaxPostData(dataString) {
    $.ajax({
      url : "post/", // the endpoint
      type : "POST",
      data : dataString, // data sent with the post request
      success : function(json) {// handle a successful response
        console.log(json)
        console.log("success") // sanity check
        var replaceTarget = json.target_instance_name
        var dom = ""
        if (json.change_privacy_level) {
          $(`#${replaceTarget}-privacy-level`).html(json.icon)
        }
        else if (json.add_new_profile_data) {
          var addTarget = json.target_instance_name
          switch (addTarget) {
            case "work-history":
              dom = createDOMWorkHistory(json)
              $(dom).insertAfter(`#${json.work_history_id} li:nth-child(1)`)
              break;
            case "related-link":
              dom = createDOMRelatedLink(json)
              $(dom).insertAfter(`#${json.related_link_id} li:nth-child(1)`)
              break;
            case "educational-bg":
              dom = createDOMEducationalBg(json)
              $(dom).insertAfter(`#${json.educational_bg_id} li:nth-child(1)`)
              break;
          }
        }
        else if (json.delete_target_instance_id) {
          var deleteTarget = json.delete_target_instance_id
          $(`#${deleteTarget}`).remove()
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
              $(`#${json.uuid}`).html(`<p>${json.introduction.replace(/\n/g, '<br>')}</p>`)
              break
            case "statement":
              $(`#${json.uuid}`).html(`<p>${json.statement.replace(/\n/g, '<br>')}</p>`)
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

  function ajaxPostUploadedFile(dataFile) {
    $.ajax({
      url : "post/", // the endpoint
      type : "POST",
      data : dataFile, // data sent with the post request
      contentType: false, // forcing jQuery not to add a Content-Type header for you, otherwise, the boundary string will be missing from it.
	    processData: false, // you must leave the processData flag set to false, otherwise, jQuery will try to convert your FormData into a string, which will fail.
      success : function(json) {// handle a successful response
        console.log(json)
        console.log("success") // sanity check
        replaceTarget = json.target_instance_name
        if (json.change_privacy_level) {
          $(`#${replaceTarget}-privacy-level`).html(json.icon)
        }
        else if (json.add_new_profile_data) {
          var addTarget = json.target_instance_name
          switch (addTarget) {
            case "portfolio":
              dom = createDOMPortfolio(json)
              $(dom).insertAfter(`#${json.portfolio_id} li:nth-child(1)`)
              break
          }
        }
        else {
          switch (replaceTarget) {
            case "cover":
              $('#profile-cover .responsive-img:first-child').css({'background-image': 'url("/media/' + json.cover + '")'})
              $('#profile-cover-bg .responsive-img').css({'background-image': 'url("/media/' + json.cover + '")'})
              break
            case "avatar":
              $('#profile-avatar img').attr('src', '/media/' + json.avatar)
              $('#menubar-avatar img').attr('src', '/media/' + json.avatar)
              break
            case "portfolio":
              $(`#${json.uuid} .profile-portfolio-title`).html(`<span>${json.title}<span class="editable-mark"><i class="fas fa-pen"></i>編集する</span></span>`)
              $(`#${json.uuid} .profile-portfolio-date`).text(`${json.made_at.slice(0, json.made_at.length-3)}`)
              $(`#${json.uuid} .profile-portfolio-link`).text(`${json.url}`)
              $(`#${json.uuid} .profile-portfolio-detail`).text(`${json.detail}`)
              if (json.image) {
                var portfolioImageElement = `#${json.uuid} .editable-data .portfolio-image`
                if ($(`${portfolioImageElement} .no-image`).length) {
                  $(`${portfolioImageElement}`).html(`
                    <div class="responsive-img" style="background-image: url('/media/${json.image}')">
                    </div>
                    `)
                }
              }
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

  function createDOMWorkHistory(json) {
    dom = `
    <li id="${json.uuid}">
      <div class="editable-data">
        <h3 class="profile-entry-title experience-organization">
          <span>
            ${json.organization}
            <span class="editable-mark"><i class="fas fa-pen"></i>編集する</span>
          </span>
        </h3>
        <p class="profile-entry-date experience-date">${json.from_date} - ${json.to_date}</p>
        <p class="profile-entry-subtitle experience-job">${json.job}</p>
        <p class="profile-entry-description experience-description">${json.experience}</p>
      </div>
      <div class="form-for-editing" style="display: none">
        <form class="post-form-to-edit-profile" method="post">
          <input type="hidden" name="target-instance-name" value="work-history">
          <input type="hidden" name="uuid" value="${json.uuid}">
          <div class="form-group">
            <div class="form-row">
              <div class="form-group col-md-6">
                <label for="${json.organization}">組織名</label>
                <input type="text" name="organization" maxlength="64" placeholder="組織名" value="${json.organization}" class="form-control" required>
              </div>
              <div class="form-group col-md-6">
                <label for="${json.job}">役職</label>
                <input type="text" name="organization" maxlength="64" placeholder="組織名" value="${json.job}" class="form-control" required>
              </div>
            </div>
            <div class="form-row">
              <label for="enrollment-period" class="col-sm-12">在籍期間</label>
              <div class="form-group col-sm">
                <input type="date" name="from_date" min="1950-01-01" max="2099-12-31" value="${json.from_date}" class="form-control">
              </div>
              <div class="form-group col-sm-1 text-center">
                -
              </div>
              <div class="form-group col-sm">
                <input type="date" name="to_date" min="1950-01-01" max="2099-12-31" value="${json.to_date}" class="form-control">
              </div>
            </div>
            <div class="form-row">
              <div class="form-group col-md-12">
                <label for="${json.experience}">事業内容など</label>
                <textarea name="experience" cols="40" rows="5" maxlength="256" class="form-control">${json.experience}</textarea>
                <div class="char-counter" data-max-length="256">
                  残り<span>256</span>文字
                </div>
              </div>
            </div>
          </div>
          <div class="form-btn">
            <button type="button" class="btn btn-link text-info delete-btn" data-toggle="modal" data-target="#delete-profile-modal" data-instance-type="work-history" data-instance-id="${json.uuid}">この項目を削除</button>
            <button type="button" class="btn btn-outline-info btn-to-cancel-editing">キャンセル</button>
            <button type="submit" class="post-button-for-profile-edit btn btn-info">更新</button>
          </div>
        </form>
      </div>
    </li>
    `
    return dom
  }
  function createDOMRelatedLink(json) {
    dom = `
    <li class="profile-related-link" id="${json.uuid}">
      <div class="editable-data">
        <h3 class="profile-related-link-title">
          <span>
          ${json.url}
            <span class="editable-mark"><i class="fas fa-pen"></i>編集する</span>
          </span>
        </h3>
      </div>
      <div class="form-for-editing" style="display: none">
        <form class="post-form-to-edit-profile" method="post">
          <input type="hidden" name="target-instance-name" value="related-link">
          <input type="hidden" name="uuid" value="${json.uuid}">
          <div class="form-group">
            <label for="${json.url}">URL</label>
            <input type="url" name="url" maxlength="256" value="${json.url}" class="form-control" required>
          </div>
          <div class="form-btn">
            <button type="button" class="btn btn-link text-info delete-btn" data-toggle="modal" data-target="#delete-profile-modal" data-instance-type="related-link" data-instance-id="${json.uuid}">この項目を削除</button>
            <button type="button" class="btn btn-outline-info btn-to-cancel-editing">キャンセル</button>
            <button type="submit" class="post-button-for-profile-edit btn btn-info">更新</button>
          </div>
        </form>
      </div>
    </li>
    `
    return dom
  }

  function createDOMEducationalBg(json) {
    dom = `
    <li id="${json.uuid}">
      <div class="editable-data">
        <h3 class="profile-entry-title education-school">
          <span>
            ${json.school}
            <span class="editable-mark"><i class="fas fa-pen"></i>編集する</span>
          </span>
        </h3>
        <p class="profile-entry-date education-graduated-at">${json.graduated_at}</p>
        <p class="profile-entry-subtitle education-major">${json.major}</p>
        <p class="profile-entry-description education-detail">${json.detail}</p>
      </div>
      <div class="form-for-editing" style="display: none">
        <form class="post-form-to-edit-profile" method="post">
          <input type="hidden" name="target-instance-name" value="educational-bg">
          <input type="hidden" name="uuid" value="${json.uuid}">
          <div class="form-group">
            <div class="form-row">
              <div class="form-group col-sm-6">
                <label for="school">学校名</label>
                <input type="text" name="school" maxlength="64" value="${json.school}" class="form-control">
              </div>
              <div class="form-group col-sm-6">
                <label for="major">学部・学科・専攻</label>
                <input type="text" name="major" maxlength="64" value="${json.major}" class="form-control" id="id_major">
              </div>
            </div>
            <div class="form-row">
              <label for="${json.graduated_at}" class="col-sm-12">卒業（予定）</label>
              <div class="form-group col-sm-6">
                <input type="date" name="graduated_at" value="${json.graduated_at}" class="form-control" id="id_graduated_at">
              </div>
            </div>
            <div class="form-row">
              <div class="form-group col-md-12">
                <label for="what-you-done">研究内容・学んだこと・課外活動・サークル</label>
                <textarea name="detail" cols="40" rows="5" maxlength="256" value="" class="form-control" id="id_detail">${json.detail}</textarea>
                <div class="char-counter" data-max-length="256">
                  残り<span>256</span>文字
                </div>
              </div>
            </div>
          </div>
          <div class="form-btn">
            <button type="button" class="btn btn-link text-info delete-btn" data-toggle="modal" data-target="#delete-profile-modal" data-instance-type="educational-bg" data-instance-id="${json.uuid}">この項目を削除</button>
            <button type="button" class="btn btn-outline-info btn-to-cancel-editing">キャンセル</button>
            <button type="submit" class="post-button-for-profile-edit btn btn-info">更新</button>
          </div>
        </form>
      </div>
    </li>
    `
    return dom
  }

  function createDOMPortfolio(json) {
    dom = `
    <li class="profile-portfolio" id="${json.uuid}">
      <div class="row editable-data">
        <div class="col-md-6">
          <div class="responsive-img-wrapper portfolio-image">
            <div class="responsive-img" style="background-image: url('/media/${json.image}')">
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <h3 class="profile-portfolio-title">
            <span>
              ${json.title}
              <span class="editable-mark"><i class="fas fa-pen"></i>編集する</span>
            </span>
          </h3>
          <p class="profile-portfolio-date">${json.made_at}</p>
          <p class="profile-portfolio-link">${json.url}</p>
          <p class="profile-portfolio-detail">${json.detail}</p>
        </div>
      </div>
      <div class="form-for-editing" style="display: none">
        <form class="post-form-to-edit-profile" method="post" enctype="multipart/form-data">
          <input type="hidden" name="target-instance-name" value="portfolio">
          <input type="hidden" name="uuid" value="${json.uuid}">
          <div class="form-group">
            <div class="form-row">
              <div class="col-md-12">
                <div class="upload-portfolio-image-btn">
                  クリックまたはドラッグ&ドロップで画像をアップロード<br>
                  JPEG / PNG / GIF形式に対応しています
                </div>
                <input type="file" name="image" accept="image/*" class="custom-file-input upload-portfolio-image">
              </div>
            </div>
            <hr>
            <div class="form-row portfolio-image-group">
              <div class="form-group col-md-3">
                <div class="responsive-img-wrapper portfolio-image">
                  <div class="responsive-img" style="background-image: url('/media/${json.image}')">
                  </div>
                </div>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group col-md-6">
                <label for="${json.title}">作品名</label>
                <input type="text" name="title" maxlength="64" value="${json.title}" class="form-control">
              </div>
              <div class="form-group col-md-6">
                <label for="${json.url}">関連URL</label>
                <input type="url" name="url" maxlength="256" value="${json.url}" class="form-control">
              </div>
            </div>
            <div class="form-row">
              <div class="form-group col-md-12">
                <label for="${json.detail}">詳細</label>
                <textarea name="detail" cols="40" rows="5" maxlength="256" value="${json.detail}" class="form-control"></textarea>
                <div class="char-counter" data-max-length="256">
                  残り<span>256</span>文字
                </div>
              </div>
            </div>
            <div class="form-row">
              <label for="${json.made_at}" class="col-sm-12">作成日</label>
              <div class="form-group col-sm-6">
                <input type="date" name="made_at" value="${json.made_at}" class="form-control" min="1950-01-01" max="2099-12-31">
              </div>
            </div>
          </div>
          <div class="form-btn">
            <button type="button" class="btn btn-link text-info delete-btn" data-toggle="modal" data-target="#delete-profile-modal" data-instance-type="portfolio" data-instance-id="${json.uuid}">この項目を削除</button>
            <button type="button" class="btn btn-outline-info btn-to-cancel-editing">キャンセル</button>
            <button type="submit" class="post-button-for-profile-edit btn btn-info">更新</button>
          </div>
        </form>
      </div>
    </li>
    `
    return dom
  }
}
