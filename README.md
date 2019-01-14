# cenote-read

>Apache Storm Topology used by cenote for querying data.

## Pipeline

* The `drpc-spout` Spout continiully listens for client requests.
* Everytime it consumes a request, it passes it down to `calculate-data` Bolt.
* This bolt (which is written in Python) read the input arguments, calculates the desired results and passes it to `return` Bolt.
* `return` Bolt, then, sends the (converted to a JSON string) result back to the client.

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

drpc.execute('read', JSON.stringify({ a: 'a', b: 7, c: true })).then(res => console.log(res)).catch(console.error);
```