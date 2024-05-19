
def Convert(string):
    return list(string.split(" "))
new_prompt = Convert(prompt)
def check_values(mylist, valu21, value2, value3):
    return valu21 in mylist and value2 in mylist and value3 in mylist


for year in range(2014, 2024):
    if check_values(new_prompt, "plot", str(year), "Sharjah"):
        charts = generate_pod_chartz(df, year, "Sharjah", "")


for year in range(2014, 2024):
    if check_values(new_prompt, "plot", str(year), "Abu Dhabi"):
        charts = generate_pod_chartz(df, year, "Abu Dhabi", "")


for year in range(2014, 2024):
    if check_values(new_prompt, "plot", str(year), "Ajman"):
        charts = generate_pod_chartz(df, year, "Ajman", "")



for year in range(2014, 2024):
    if check_values(new_prompt, "plot", str(year), "Al Fujairah"):
        charts = generate_pod_chartz(df, year, "Al Fujairah", "")


for year in range(2014, 2024):
    if check_values(new_prompt, "plot", str(year), "Umm al-Quwain"):
        charts = generate_pod_chartz(df, year, "Umm al-Quwain", "")


for year in range(2014, 2024):
    if check_values(new_prompt, "plot", str(year), "Dubai"):
        charts = generate_pod_chartz(df, year, "Dubai", "")


for year in range(2014, 2024):
    if check_values(new_prompt, "plot", str(year), "Ras Al Khaimah"):
        charts = generate_pod_chartz(df, year, "Ras Al Khaimah", "")


for year in range(2014, 2024):
    if check_values(new_prompt, "plot", str(year), "Female"):
        charts = generate_pod_chartz(df, year, "", "Female")


for year in range(2014, 2024):
    if check_values(new_prompt, "plot", str(year), "male"):
        charts = generate_pod_chartz(df, year, "", "male")

for year in range(2014, 2024):
    if check_values(new_prompt, "plot", str(year), "Mentality"):
        charts = generate_pod_chartz(df, year, "", "Mentality")

for year in range(2014, 2024):
    if check_values(new_prompt, "plot", str(year), "Auditory"):
        charts = generate_pod_chartz(df, year, "", "Auditory")
for year in range(2014, 2024):
    if check_values(new_prompt, "plot", str(year), "Autism"):
        charts = generate_pod_chartz(df, year, "", "Autism")

for year in range(2014, 2024):
    if check_values(new_prompt, "plot", str(year), "Physical"):
        charts = generate_pod_chartz(df, year, "", "Physical")

for year in range(2014, 2024):
    if check_values(new_prompt, "plot", str(year), "Multiple"):
        charts = generate_pod_chartz(df, year, "", "Multiple")

