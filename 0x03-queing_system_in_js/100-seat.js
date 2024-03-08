import { createClient } from 'redis';
import util from 'util';
import express from 'express';
import kue from 'kue';

const client = createClient();
const clientGet = util.promisify(client.get).bind(client);
let reservationEnabled = true;

async function reserveSeat (number) {
  const availableSeats = await clientGet('available_seats');
  client.set('available_seats', availableSeats - number);
}

async function getCurrentAvailableSeats () {
  return await clientGet('available_seats');
}

const queue = kue.createQueue();
const app = express();
const port = 1245;

client.set('available_seats', 50);

app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();

  res.json({ numberOfAvailableSeats: availableSeats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
  } else {
    const job = queue.create('reserve_seat');

    job.on('enqueue', () => {
      res.json({ status: 'Reservation in process' });
    });

    job.on('complete', (result) => {
      console.log(`Seat reservation job ${job.id} completed`);
    });

    job.on('failed', (errorMessage) => {
      console.log(`Seat reservation job ${job.id} failed: `, errorMessage);
    });

    job.save();
  }
});

app.get('/process', (req, res) => {
  queue.process('reserve_seat', (job, done) => {
    reserveSeat(1)
      .then(() => {
        getCurrentAvailableSeats()
          .then((result) => {
            if (result <= 0) {
              reservationEnabled = false;
            }
            if (result >= 0) {
              done();
            } else {
              done(new Error('Not enough seats available'));
            }
          });
      });
  });
  res.json({ status: 'Queue processing' });
});

app.listen(port, () => {
  console.log('...');
});
