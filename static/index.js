document.addEventListener("DOMContentLoaded", () => {

  // Colours for the clans
  const blue_color = '#0B4F6C'
  const green_color = '#168F66'
  const yellow_color = '#FFD447'

  // If you are trying to get the password, good luck with this sha256 hash!
  let password_hashed = "3147a76e604d5737c45bfe2209eb58399519ecde60a121a2c396779b577fbd1d"

  function change_to(div) {
    if ($(div).css("display") == "none") {
      let all_children = document.querySelector("#all").children
      for (let i = 0; i < all_children.length; i++) {
        $(all_children[i]).fadeOut()
      }
      setTimeout(() => {
        $(div).fadeIn()
      }, 400)
    }
  }

  // Buttons configure
  $("#add_points_link").click(() => {
    change_to("#add_points_div")
    $("body").css("backgroundColor", "white")
  })
  $("#main_link").click(() => {
    change_to("#main_div")
    $("body").css("backgroundColor", "black")
  })

  // Create drawing instance
  let draw = SVG('drawing');
  // Add chart bars
  var left_rect = draw.rect("31%")
                    .attr({ fill: blue_color })
                    .flip("y")
                    .dy("-100%")
                    .radius(10)
  var middle_rect = draw.rect("31%")
                      .x(window.innerWidth / 3)
                      .attr({ fill: green_color })
                      .flip("y")
                      .dy("-100%")
                      .radius(10)
  var right_rect = draw.rect("31%")
                    .x(2 * window.innerWidth / 3)
                    .attr({ fill: yellow_color })
                    .flip("y")
                    .dy("-100%")
                    .radius(10)
  var clan_id = {
    "P": "poseidon",
    "H": "hydra",
    "U": "ulysse"
  }
  var rect_id = {
    "P": left_rect,
    "H": middle_rect,
    "U": right_rect
  }

  // Initial setup
  children = document.querySelector("#hide").children
  var points = []
  for (let i = 0; i < children.length; i++) {
    clan = children[i].dataset["clan"]
    points = [children[i].dataset["points"], children[i].dataset["percent"]]
    update_points(clan, points, text_update=true)
  }
  // Make initial transition smooth
  $("#drawing").animate({ opacity: 1 }, 500)

  // Number counting up options
  var options = {
    useEasing: true,
    useGrouping: true,
    separator: ',',
    decimal: '.',
  }

  document.querySelector("#add_points_form").onsubmit = () => {
    if (sha256(document.querySelector("#points_password").value) != password_hashed) {
      document.querySelector("#alert").innerHTML = "Désolé, le mot de passe était incorrecte."
      document.querySelector("#alert").style.display = "block"
      return false
    }
  }

  function update_points(id, number, text_update) {
    if (text_update) {
      // Update number
      current = document.querySelector("#" + clan_id[id]).innerHTML
      current = parseInt(current.replace(',',''))
      var count = new CountUp(clan_id[id], current, number[0], 0, 2.5, options)
      if (!count.error) {
        count.start()
      } else {
        console.error(count.error)
      }
    }
    // Update rect
    rect_id[id].animate().height(number[1] + '%')
  }

  // Initial window calibration
  document.querySelector("#main_div").style.height = (window.innerHeight - 180) + "px";

  // Calibrate positioning when window is resized
  window.onresize = () => {
    middle_rect.x(window.innerWidth / 3)
    right_rect.x(2 * window.innerWidth / 3)

    document.querySelector("#main_div").style.height = (window.innerHeight - 180) + "px";
  }
})
