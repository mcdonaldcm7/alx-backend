import kue from 'kue';

const blacklist = ['4153518780', '4153518781'];
const queue = kue.createQueue();

function sendNotification (phoneNumber, message, job, done) {
  let progress = 0;
  job.progress(progress, 100);
  if (blacklist.includes(phoneNumber)) {
    return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  }

  progress += 50;
  job.progress(progress, 100);
  done();
}

queue.process('push_notification_code_2', 2, (job, done) => {
  sendNotification(job.data.phoneNumber, job.data.message, job, done);
});
