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

  document.querySelector("#add_points_link").onclick = () => {
    change_to(document.querySelector("#add_points_div"))
  }

  document.querySelector("#main_link").onclick = () => {
    change_to(document.querySelector("#main_div"))
  }

  var clan_names = {
    "R": "Volcans (7-8)",
    "B": "Avalanches (9-10)",
    "N": "Éclairs (11-12)",
    "G": "Cyclones (Adultes)",
  }

  var clan_colors = {
    "R": 'rgba(255, 56, 56, 0.8)',
    "B": 'rgba(242, 242, 242, 0.8)',
    "N": 'rgba(31, 31, 31, 0.8)',
    "G": 'rgba(115, 115, 115, 0.8)',
  }

  var labels = []
  var colors = []
  var data = []

  $("#hide").children().each((i, obj) => {
    labels.push(clan_names[obj.dataset.clan])
    colors.push(clan_colors[obj.dataset.clan])
    data.push(obj.dataset.points)
  })
  // Create chart
  var chart = document.querySelector("#myChart")
  var myChart = new Chart(chart, {
      type: 'bar',
      data: {
          labels: labels,
          datasets: [
            {
              backgroundColor: colors,
              data: data,
              borderWidth: 3,
          }
        ]
      },
      options: {
          legend: {
            display: false,
          },
          scales: {
              xAxes: [{
                ticks: {
                    fontSize: 15,
                }
              }],
              yAxes: [{
                scaleLabel: {
                  display: true,
                  labelString: 'Points'
                },
                ticks: {
                    fontSize: 13,
                    beginAtZero: true
                }
              }]
          }
      }
  });

  document.querySelector("#add_points_form").onsubmit = () => {
    if (sha256(document.querySelector("#points_password").value) != password_hashed) {
      document.querySelector("#alert").innerHTML = "Désolé, le mot de passe était incorrecte."
      document.querySelector("#alert").style.display = "block"
      return false
    }
  }
})
