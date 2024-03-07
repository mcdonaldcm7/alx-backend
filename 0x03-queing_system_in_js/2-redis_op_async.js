import { createClient } from 'redis';
import util from 'util';

const client = createClient();

client.on('error', (err) => {
  console.log('Redis client not connected to the server: ', err);
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, (err, reply) => {
    if (err) {
      console.error(err);
      return;
    }
    console.log('Reply:', reply);
  });
}

/*async function displaySchoolValue(schoolName) {
  const promiseGets = util.promisify(client.get).bind(client);
  const reply = await promiseGets(schoolName);
   console.log(reply);
}*/

const clientGet = util.promisify(client.get).bind(client);

const displaySchoolValue = async (schoolName) => {
  const reply = await clientGet(schoolName);
  console.log(reply);
}

async function displayAndSet() {
  await displaySchoolValue('Holberton');
  setNewSchool('HolbertonSanFrancisco', '100');
  await displaySchoolValue('HolbertonSanFrancisco');
}

displayAndSet();
