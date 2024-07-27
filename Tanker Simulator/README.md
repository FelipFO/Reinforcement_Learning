# Tanker Ship Problem Control

Este repositorio contiene los códigos necesarios para replicar los experimentos del problema
_Tanker Ship_ propuesto por Kevin Passino en su libro Biomimicry for Optimization, Control 
and Automation. A la fecha hay dos tipos de controlador implementados:

1. Red Neuronal 
2. Red Neuronal tipo RBF

##  Uso del repositorio

El repositorio está dividido en tres partes principales

### Simulator

El archivo `simulator.py` implementa la logica de la simulación. Para esto, se apalanca 
de los modulos `controller` y `tanker`. Si se desea replicar los resultados del libro,
el usuario debe realizar minimas modificaciones a este archivo definiendo los 
parámetros de simulación.

#### Parámetros
1. `mode`: Este parámetro hace referencia a la carga del barco, siendo "ballast" el comportamiento nominal mientras que 
   "full" simula un barco más ligero el cual es más difícil de controlar.
   
2. `ctrl_name`: Este parámetro es el nombre del controlador a utilizar actualmente se soporta "nn" y "rbf"

3. `simulation_steps`: Este parámetro indica el número de pasos que seran simulados, se recomiendan simulaciones de 
   por lo menos 4000 pasos. 
   
4. `sampling_interval`: Este parámetro hace referencia al intervalo de muestreo del controlador. Indica la frecuencia
con la que se actualizara la señal de control.  
   
5. `initial_conditions`: Estas son las condiciones iniciales del sistema en el orden [x1, x2, x3] 

Una vez son definidos los parámetros de simulación se debe ejecutar el archivo con la instruccion mostrada a continuación 
o con el IDE de su preferencia

```
cd root/to/tanker
python simulator.py
```

### Tanker

El archivo `tanker/tanker.py` implementa el sistema dinámico del _Tanker_ como es especificado en el libro 
de Kevin. Para simular este sistema se utiliza el método de Runge-Kutta de cuarto orden. 
Para información más detallada sobre este algoritmo consulte la página 120 del libro.

### Controllers

Cada uno de los controladores está implementado como un archivo independiente dentro del módulo `controllers`.
 Ambos controladores siguen un patron de diseño predefinido.

#### Construtor

En el constructor se definen los parámetros del modelo.

#### predict()

Este método computa la señal de control basado en la referencia y el estado del sistema. 

#### plot_in_out_map()

Este metodo grafica el mapeo entre entrada y salida del controlador. 

## Modificar controladores existentes.

Para modificar el comportamiento de los controladores implementados, el usuario solo debe modificar 
el valor de los parámetros de cada modelo en el constructor del mismo y ejecutar el archivo `simulator.py` como fue 
descrito anteriormente.

## Crear nuevos controladores

Si se desea añadir nuevos controladores, se recomienda describir el controlador en un nuevo archivo en 
el módulo `controllers` siguiendo el patron de diseño expuesto anteriormente. De esta manera, añadirlo en el archivo 
`simulator.py` será transparente. 
