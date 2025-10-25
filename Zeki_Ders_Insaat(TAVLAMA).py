import random 
import math

jobs = [
    {"job": "Temel", "duration": 5, "material_cost": 1000},
    {"job": "Duvar", "duration": 7, "material_cost": 1500},
    {"job": "Cati", "duration": 4, "material_cost": 1200},
    {"job": "Zemin", "duration": 3, "material_cost": 800},
]

# Günlük çalışma kapasitesi (saat cinsinden)
work_capacity = 3

# Başlangıç çözümü
def initial_solution():
    solution = jobs[:]
    random.shuffle(solution)
    return solution

# Maliyet fonksiyonu
def cost_function(solution):
    total_duration = 0 # Tüm iş süreleri toplamı
    total_material_cost = 0 # Tüm malzemelerin toplam maliyeti 
    total_labor_cost = 0 # Tüm işçilerin toplam iş gücü maliyeti
    project_duration = 0 # Projenin toplam süresi
    
    for job in solution:
        total_material_cost += job["material_cost"]
        labor_cost = job["duration"] * work_capacity * 50
        total_labor_cost += labor_cost
        total_duration += job["duration"]
    
    project_duration = total_duration
    
    # Proje maliyeti = malzeme maliyeti + iş gücü maliyeti + süre cezası
    delay_penalty = 0
    if project_duration > 30:
        delay_penalty = (project_duration - 30) * 100 # Gecikme başına ceza 
    
    total_cost = total_material_cost + total_labor_cost + delay_penalty
    return total_cost, total_duration

# Komşu çözüm (random 2 işin yerini değiştirerek yeni bir çözüm oluşturur)
def neighbor(solution):
    new_solution = solution[:]
    i, j = random.sample(range(len(solution)), 2)
    new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
    return new_solution   

# Tavlama Algoritması
def simulated_annealing(initial_temp, cooling_rate, max_iterations):
    current_solution = initial_solution()
    current_cost, current_duration = cost_function(current_solution)
    best_solution = current_solution
    best_cost = current_cost
    temperature = initial_temp
    
    for iteration in range(max_iterations):
        # Iterasyon sayısı boyunca yeni komşu çözümler oluştur
        new_solution = neighbor(current_solution)
        new_cost, new_duration = cost_function(new_solution)
        
        if new_cost < current_cost:
            current_solution = new_solution
            current_cost = new_cost
        
        else:
            # Kötü çözümler tavlama olasılığı ile kabul edilebilir
            acceptance_prob = math.exp((current_cost - new_cost) / temperature)
            if random.random() < acceptance_prob:
                current_solution = new_solution
                current_cost = new_cost
        
        # Eğer yeni çözüm daha iyiyse en iyi çözümü güncelle
        if current_cost < best_cost:
            best_solution = current_solution
            best_cost = current_cost
        
        # Sıcaklık soğutma katsayısı
        temperature *= cooling_rate
    
    return best_solution, best_cost

# Parametreler
initial_temp = 1000 # Başlangıç sıcaklığı
cooling_rate = 0.99 # Soğuma katsayısı
max_iterations = 1000 # Maksimum iterasyon sayısı

# Tavlama algoritmasını çalıştır
best_solution, best_cost = simulated_annealing(initial_temp, cooling_rate, max_iterations)

print("En iyi çözüm: ")
for job in best_solution:
    print(f"{job['job']}: Süre = {job['duration']} gün, Maliyet = {job['material_cost']} TL")

total_cost, total_duration = cost_function(best_solution)
print(f"Toplam Maliyet: {total_cost} TL")
print(f"Toplam Süre: {total_duration} gün")
