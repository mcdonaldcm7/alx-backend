import createPushNotificationJobs from './8-job';
import kue from 'kue';
import chai from 'chai';

const queue = kue.createQueue();
const expect = chai.expect;

queue.testMode.enter(true);

describe('createPushNotificationsJobs', function() {
  it('display a error message if jobs is not an array', function() {
    const jobs = 'Not an Array';

    expect(() => createPushNotificationJobs(jobs, queue)).to.throw();
  });

  it('create two new jobs on the queue', function() {
    const jobs = [
      { job: 1, msg: 'First test' },
      { job: 2, msg: 'Second test' }
    ];

    createPushNotificationJobs(jobs, queue);

    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_3');
    expect(queue.testMode.jobs[0].data).to.eql({ job: 1, msg: 'First test' });
    expect(queue.testMode.jobs[1].type).to.equal('push_notification_3');
    expect(queue.testMode.jobs[1].data).to.eql({ job: 2, msg: 'Second test' });
  });
});
