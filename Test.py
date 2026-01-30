import billboard
chart = billboard.ChartData("hot-100-songs", year=2007)
for i, s in enumerate(chart):
    if i >= 5:
        break
    print(s.rank, s.title, s.artist)