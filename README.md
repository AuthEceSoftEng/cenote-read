# cenote-read

>Apache Storm Topology used by cenote for querying data.

## Run to a cluster

* Compile the source code:

```bash
$ mvn clean package
```

* Submit the topology to the cluster:

```bash
$ storm jar path/to/read-0.1.0-jar-with-dependencies.jar com.issel.cenote.ReadTopology ReadTopology
```

## Execute functions through a client

```javascript
const drpcjs = require('drpcjs');
const drpc = new drpcjs({ host: '83.212.104.172' }); // Using DNS records (e.g. snf-{...}) won't work.

drpc.execute('read', 'something').then(res => console.log(res)).catch(console.error);
```