<h2>
  Lab work 3
</h2>
  <p>During the laboratory work, a serializer was implemented. The resulting serializer correctly serializes (saves/packs) and deserializes (restores/unpacks) the stored information.<p>
  <p>The program code contains a factory method create_serializer(), which generates various types of serializers. It is possible to easily add a new serializer without changing the architecture of the application.<p>

Each of the serializers implements the following methods:
<ul>
 <li>dump(obj, fp) - serializes Python objects to file</li>
 <li>dump(obj, fp) - serializes Python objects to file</li>
 <li>lload(fp) - deserializes Python objects from file </li>
 <li>load(fp) - deserializes Python objects from file </li>
</ul>

Serialization/deserialization works for the following objects:
<ul>
  <li>primitive objects</li>
 <li>class</li>
 <li>objects with simple fields</li>
 <li>objects with complex fields and functions</li>
 <li>functions (including recursive)</li>
</ul>
