import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, Image } from 'react-native';
import ModalDropdown from 'react-native-modal-dropdown';
import { initializeApp } from 'firebase/app';
import { getDatabase, ref, onValue } from 'firebase/database';
import axios from 'axios';


export default function App() {
  // Estados para almacenar los valores de sensores y la planta seleccionada
  const [humedad, setHumedad] = useState(0);
  const [movimiento, setMovimiento] = useState(0);
  const [temperatura, setTemperatura] = useState(0);
  const [selectedPlant, setSelectedPlant] = useState('Tomate'); // Elige un valor predeterminado
  const [plantDetails, setPlantDetails] = useState({});  // Nuevo estado para almacenar detalles de la planta
  const [plantNames, setPlantNames] = useState([]);

  const firebaseConfig = {
    // Configuración de Firebase con las credenciales de tu proyecto
    apiKey: "AIzaSyAt5_BrZyNPK2hoLvBXMDjeyAY9pOmNqsY",
    authDomain: "gardensense-cfe37.firebaseapp.com",
    databaseURL: "https://gardensense-cfe37-default-rtdb.firebaseio.com",
    projectId: "gardensense-cfe37",
    storageBucket: "gardensense-cfe37.appspot.com",
    messagingSenderId: "949510113189",
    appId: "1:949510113189:web:94c542b2d64df8fc2c4a4c",
    measurementId: "G-0TR1T5V5ZP"
  };
  // Inicializa la aplicación de Firebase
  const firebaseApp = initializeApp(firebaseConfig);
  const db = getDatabase(firebaseApp);
  const sensoresRef = ref(db, 'sensores');

  useEffect(() => {
    // Escucha cambios en la base de datos de Firebase y actualiza los estados
    onValue(sensoresRef, (snapshot) => {
      const data = snapshot.val();
      setHumedad(data.humedad);
      setMovimiento(data.movimiento);
      setTemperatura(data.temperatura);
    });

    // Realizar la solicitud a la API al cargar la planta seleccionada
    getPlantDetails(selectedPlant);

    // Realizar solicitud a la API para obtener nombres de plantas
    fetch("https://fastapi-production-0454.up.railway.app/plantas/nombres")
      .then(response => response.json())
      .then(data => setPlantNames(data))
      .catch(error => console.error("Error al obtener nombres de plantas:", error));

  }, [selectedPlant]);  // Agrega selectedPlant como dependencia

  const getPlantDetails = async (plantName) => {
    try {
      // Realizar una solicitud a la API para obtener detalles de la planta
      const response = await axios.get(`https://fastapi-production-0454.up.railway.app/plantas/${plantName}`);
      setPlantDetails(response.data);  // Actualizar el estado con los detalles de la planta
    } catch (error) {
      console.error('Error al obtener detalles de la planta:', error);
    }
  };
 
  return (
    <View style={styles.container}>
      {/* Encabezado de la aplicación */}
      <View style={styles.header}>
        <Image source={require('./images/options.png')} style={styles.options} />
        <View style={styles.home}>
          <Text style={styles.headerText}>Home</Text>
        </View>
      </View>

      <View style={styles.content}>
        {/* Información de la planta seleccionada */}
        <View style={styles.plantInfoContainer}>
          <View style={styles.menuIconContainer}>
            {/* Selector de planta desplegable */}
            <ModalDropdown
              options={plantNames}
              initialScrollIndex={0}
              onSelect={(index, value) => setSelectedPlant(value)}
              dropdownStyle={styles.dropdown}
            >
              <Image source={require('./images/toggle.png')} style={styles.dropdownOptionImage} />
            </ModalDropdown>
          </View>
          <View style={styles.plantName}>
            <Text style={styles.Text}>{selectedPlant}</Text>
          </View>
        </View>

        {/* Contenedor de información de sensores */}
        <View style={styles.rectangleContainer}>
          {/* Línea de separación */}
          <View style={styles.line}>
            <View style={styles.lineBorder}></View>
          </View>

          {/* Muestra la humedad del sensor */}
          <View style={styles.rectangle}>
            <Text style={[
              styles.rectangleText,
              // Cambia el color y el mensaje basado en la humedad
              humedad > plantDetails.maxhum
                ? { color: 'navy' }
                : humedad < plantDetails.minhum
                ? { color: 'yellow' }
                : null,
            ]}>
              {humedad > plantDetails.maxhum
                ? 'Mucha agua'
                : humedad < plantDetails.minhum
                ? 'Falta regar'
                : 'Regada'}
            </Text>
          </View>

          {/* Muestra el estado de movimiento del sensor */}
          <View style={styles.rectangle}>
            <Text style={[styles.rectangleText, movimiento === 1 ? { color: 'red' } : null]}>
              {movimiento === 0 ? 'A salvo' : '¡Cuidado!'}
            </Text>
          </View>

          {/* Muestra la temperatura del sensor */}
          <View style={styles.rectangle}>
            <Text style={[styles.rectangleText, 
                        temperatura > plantDetails.maxtemp ? { color: 'orange' } : (temperatura < plantDetails.mintemp ? { color: 'skyblue' } : null)]}>
              {temperatura} °C
            </Text>
          </View>
          
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#E4E4D0',
  },
  header: {
    height: 90,
    flexDirection: 'row',
    alignItems: 'center',
  },
  headerText: {
    fontSize: 30,
    fontWeight: 'bold',
    color: '#fff',
  },
  home: {
    paddingVertical: 27,
    backgroundColor: "#94A684",
    flex: 1,
    alignItems: 'center',
    borderBottomLeftRadius: 30,
  },
  options: {
    marginTop: 10,
    marginLeft: 20,
    marginRight: 160,
  },
  pickerContainer: {
    top: 0,
    left: 0,
    right: 0,
    zIndex: 1,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  rectangleContainer: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  rectangle: {
    width: 300,
    height: 100,
    backgroundColor: '#B3A492',
    justifyContent: 'center',
    alignItems: 'center',
    margin: 10,
    borderRadius: 10,
  },
  rectangleText: {
    fontSize: 30,
    fontWeight: 'bold',
    color: '#fff',
  },
  line: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  lineBorder: {
    flex: 1,
    height: 2,
    backgroundColor: '#94A684',
  },
  plantInfoContainer: {
    flexDirection: 'row', // Esto establece la dirección de fila
    alignItems: 'center', // Esto alinea los elementos verticalmente en el centro
  },
  // Estilos para el nombre de la planta
  plantName: {
    flex: 1,
    marginLeft: 10,
  },
  Text: {
    fontSize: 30,
    fontWeight: 'bold',
    color: '#fff',
  },
  // Estilos para el contenedor del menú del picker
  menuIconContainer: {
    paddingLeft: 10,
  },
  // Estilos para el menú desplegable
  dropdownOptionImage: {
    width: 30,
    height: 35,
  },
  dropdown: {
    width: 100,
    height: 100,
    borderColor: 'transparent',
    borderWidth: 0,
    borderRadius: 3,
    backgroundColor: '#94A684',
  },
});

