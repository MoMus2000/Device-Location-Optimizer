from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpBinary

# Define hypervisors and their vCPU counts
hypervisors = {
        "H1": {"vcpu": 128, "priority": 3,  "ram": 128},  # Lower priority number means higher priority
        "H2": {"vcpu": 108, "priority": 2,  "ram": 64},
        "H3": {"vcpu": 10 , "priority": 5,  "ram": 32},
        "H4": {"vcpu": 25 , "priority": 1,  "ram": 16},
        "H5": {"vcpu": 24 , "priority": 2,  "ram": 8 },
}


location = {
    "H1": "Toronto" ,
    "H2": "Montreal",
    "H3": "Calgary" ,
    "H4": "Edmonton"
}

required_vcpus = 100
required_ram   = 33

# Weights for the objective function
alpha = 1.0  # Weight for vCPU difference
beta = 2.0   # Weight for priority (adjust to control influence)

# Define the problem
prob = LpProblem("Hypervisor_Selection_With_Priority", LpMinimize)

# Decision variables
x = {h: LpVariable(f"x_{h}", cat=LpBinary) for h in hypervisors}

# Objective function: Minimize vCPU difference and prioritize location
prob += lpSum((alpha * abs(hypervisors[h]["vcpu"] - required_vcpus) + 
               alpha * abs(hypervisors[h]["ram"]  - required_ram)   +
               beta * hypervisors[h]["priority"]) * x[h] for h in hypervisors)

# Constraint: Exactly one hypervisor must be selected
prob += lpSum(x.values()) >= 2 

# Constraint: Ensure only hypervisors with at least 12 vCPUs can be chosen
prob += lpSum(x[h] for h in hypervisors if hypervisors[h]["vcpu"] < required_vcpus) == 0
prob += lpSum(x[h] for h in hypervisors if hypervisors[h]["ram"] < required_ram) == 0

# Solve the problem
prob.solve()

# Output the selected hypervisor
selected_hypervisor = [h for h in hypervisors if x[h].value() == 1]

for h in hypervisors:
    print(x[h].value())
print(selected_hypervisor)

selected_hypervisor = [h for h in hypervisors if x[h].value() == 1][0]
print(f"Selected Hypervisor: {selected_hypervisor} with {hypervisors[selected_hypervisor]['vcpu']} vCPUs")

