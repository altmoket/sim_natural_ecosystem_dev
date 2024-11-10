# Simulación del desarrollo de un ecosistema natural.
## Project Overview
The Natural Ecosystem Simulation project aims to create an ecosystem to simulate the evolutionary processes of various species that interact with each other and their environment. The species do not need to be inspired by real-life organisms but should possess specific characteristics that allow them to integrate into the ecosystem.

## Team Members
- **[Dianelys Cruz Mengana](https://github.com/DianeMC)** (C-311)
- **[Leandro Hernández Nuñez](https://github.com/altmoket)** (C-312)
- **[Jordan Pla González](https://github.com/jordipynb)** (C-311)

## Central Idea
The project focuses on generating a natural, non-deterministic system that provides specific data centered on the characteristics, behavior, and interaction of species in a moderately hostile yet easily adjustable environment.

## Documentation: [HERE](https://github.com/altmoket/sim_natural_ecosystem_dev/blob/main/docs/description.md)   
	
## Requirements

### Mandatory Requirements
* Install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* Install [Python3](https://www.python.org/downloads/)
* Install **scipy** `pip install scipy`
<!-- * Install [pipenv](https://pypi.org/project/pipenv/) -->
* Clone the repository `git clone "https://github.com/altmoket/sim_natural_ecosystem_dev.git"`
* Navigate to the project directory `cd sim_natural_ecosystem_dev/`
<!-- * Activar el environment `pipenv shell`
* Instalar paquetes necesarios `pipenv install` -->
### Optional Requirements:
* Install **pytest** `pip install pytest`

## Execution Methods:
### Basic Execution
* To run the simulation, use the following command:
```python
python main.py
```

### Running Tests
* To execute the tests, use:
```python
python -m pytest
```

## Fundamental Characteristics of the Project
The project creates a pure, non-deterministic natural system that focuses on the characteristics, behavior, and interaction of species in a moderately hostile environment that can be easily adjusted. The world where different species interact consists of zones with specific habitats and characteristics; these zones also have an adjacency list with other zones and the distances between them.

To generate this map, you can use the following instruction:
```python
zones = WorldGenerator().generate(min, max)  # Generates X number of zones between min and max values.
```
### Initial Population Setup
At the beginning of the simulation, animals are introduced into the world using a Constraint Satisfaction Problem (CSP) approach to ensure that it is not overly hostile initially. This considers restrictions on placing species in favorable zones and as far away as possible from their predators (not in their zone or in immediately adjacent zones).

### Habitat Types
The project includes several habitat types: Polar, Temperate, Tropical, and Desert. For example:

- **Polar Habitat**: Features temperatures uniformly distributed between -5 and 10°C, with vegetation abundance also uniformly distributed between 65% and 80%.

Similar principles apply to other habitats but with their unique characteristics that are vital for each zone.

### Environmental Events
Various discrete events occur in the ecosystem where the waiting time for another event of the same type follows an exponential distribution:

- **Animal Birth**: The likelihood of this event occurring is maximized if mating animals are of the same species and different sexes, are in a favorable habitat zone, and there is a higher population density of that species in the area.
  
- **Animal Death**: This event acts as a "God" establishing equilibrium in the ecosystem to prevent overpopulation. This value can be adjusted based on specific thresholds defined for overpopulation.

- **Heat Waves**: These introduce changes to the environment, encouraging animals to migrate to more favorable zones if they are currently in unsuitable areas.

- **Cold Waves**: Similar to heat waves but induce opposite effects.

## Interaction Between Species
The project adopts an agent-based approach using both Purely Reactive Agents and Intelligent Agents to enhance result variability. The animals created do not need to follow real-world patterns; they can be fictional. For any new species added to the ecosystem, they must adhere to certain rules:

- Behave as some type of Agent (inheritance).
- Specify favorable habitats (method `<habitat>`).
- Define the percentage of vegetation consumed when feeding from the environment (method `<feed_on_vegetation>`).
- Establish lifespan ranges (method `<life_expectancy>`).
- Define speed ranges (method `<speed>`).
- Specify prey species (method `<prey>`).
- Specify predator species (method `<depredator>`).
- Define uninhabitable habitats and health percentages lost from inhabiting them (method `<uninhabitable>`).
- Define health loss percentage due to malnutrition (method `<desnutrition>`).

### Decision-Making Actions
Implemented actions for agent decision-making include:

- Feeding (from the environment or other animals).
- Migrating (to favorable zones or fleeing from predators).
- Dying (due to low health or end of lifespan).
- Doing nothing.

To facilitate varied behaviors and actions, we developed:

- **Ant Colony**: For food-seeking behavior in Intelligent Agents; Purely Reactive Agents explore for food.
- **A***: For finding favorable zones without immediate predators; utilized by both agent types with different heuristics.

## Simulation Results
Results were obtained over a simulated period of three years across various scenarios with a total of 30 tests conducted:

### Predator Numbers
When predators exceed 30% of total species present, mass extinction occurs in 80% of cases. This percentage varies depending on the number of zones; more zones improved results by 30% in some tests.

### Number of Zones
Increasing zone numbers leads to more food availability for herbivores, resulting in fewer deaths from malnutrition. A higher number of zones also reduces negative mutation effects on habitats, leading to increased habitability and stability within the system. Tests varied zone numbers from 12 to 17; with fewer zones (3-8), mass extinctions occurred in 65% of cases.

## Conclusion
The majority of scenarios tend to become unfavorable for evolution; an excessively changing environment is detrimental to proper development. Key improvements occur when:

- The number of predators is less than 25% of the total species.
- The number of zones is high (between 12 and 17).
- Abundant vegetation exists.

In other cases, the system remains hostile.

This documentation provides a comprehensive overview of the Natural Ecosystem Simulation project, detailing its objectives, methods, characteristics, events within the ecosystem, and key findings from simulations.
