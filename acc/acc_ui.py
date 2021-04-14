import acc
from browser import window, document
import editor
import math

hell_element = document.getElementById("hell")
#status_element = document.getElementById("status")
#ai_move_element = document.getElementById("ai_move")

speed_element = document.getElementById("speed_element")
speed_plot = window.SmoothieChart.new()
speed_plot.streamTo(document.getElementById("speedgraph"));
speed_plot.stop()

import inspect
from algos_gen import algorithms
algos_el = document.getElementById("algos")
for name, src in algorithms.items():
    el = document.createElement("option")
    el.innerHTML = name
    algos_el.appendChild(el)

base_accelerator = None

def set_algo(ev):
    global base_accelerator
    code = algorithms[algos_el.value]
    editor.editor.setValue(code)
    exec(code, acc.__dict__, locals())
    base_accelerator = acceleration

algos_el.bind("change", set_algo)
set_algo(None)
n_vehicles = 3
noise = 0
lag = 0
start_velocity = 0
play = False

def reset():
    global hell
    hell_element.innerHTML = ""

    n_vehicles = int(document.getElementById("nvehicles").value)
    lag = int(document.getElementById("lag").value)
    noise = float(document.getElementById("noise").value)
    
    hell = acc.RoadToHell(length=100.0)
    base_a = base_accelerator
    for i in range(n_vehicles):
        a = base_a
        #a = acc.lagger(a, lag)
        #a = acc.noiser(a, noise)
        v = hell.add_vehicle(a)
        v.velocity = start_velocity
        el = document.createElement("div")
        el.innerHTML = ">"
        hell_element.appendChild(el)
        v.el = el
        v.speedseries = window.TimeSeries.new()
        speed_plot.addTimeSeries(v.speedseries)
    hell.spread_equally()
    render()

def step(dt):
    dt = dt/1e6
    hell.step(1/60) # Hack
    render()
    if play:
        window.requestAnimationFrame(step)

def render():
    time = hell.time
    for v in hell.vehicles:
        angle = v.position/hell.length*2*math.pi
        x = math.sin(angle)
        y = math.cos(angle)
        x += 1.0; x /= 2.0
        y += 1.0; y /= 2.0
        v.el.style.left = f"{x*100}%"
        v.el.style.top = f"{y*100}%"
        v.el.style.transform = f"rotate({-angle/math.pi*180}deg)"
        v.speedseries.append(time, v.velocity)
#new_game()

def toggle_play():
    global play
    if not play:
        play = True
        step(0)
        speed_plot.start()
    else:
        play = False
        speed_plot.stop()

document.getElementById("start").addEventListener("click", lambda *x: toggle_play())
document.getElementById("reset").addEventListener("click", lambda *x: reset())
reset()
#tictactoe.random_game()


