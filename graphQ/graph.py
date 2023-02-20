import requests
import json
import graphql
import re
from graphQ.matrix import Matrix
DEFAULT_REGEX = "|".join(
    [
        r"pass",
        r"pwd",
        r"user",
        r"email",
        r"key",
        r"config",
        r"secret",
        r"cred",
        r"env",
        r"api",
        r"hook",
        r"token",
        r"hash",
        r"salt",
    ]
)

class Graph:
    def __init__(self,introspection=None,url=None,file_path=None,additional_headers=None):
        if url:
            introspection = remote_introspection(url,additional_headers)["data"]
        elif file_path:
            with open(file_path) as f:
                introspection = json.load(f)
        elif introspection:
            introspection = introspection
        self.schema = load_introspection(introspection)
    def to_matrix(self):
        def get_name(o):
            try:
                return o.name
            except:
                return get_name(o.of_type)
        self.schema.get_type_map().keys()
        trimmed = [k for k,v in self.schema.get_type_map().items() if isinstance(v,graphql.type.definition.GraphQLObjectType) and not k.startswith("__")]
        mapping = {k:idx for idx,k in enumerate(trimmed)}
        function_roots = [i.name for i in [self.schema.get_query_type(),self.schema.get_mutation_type(),self.schema.get_subscription_type()] if i]
        matrix = Matrix()
        for obj_name in trimmed:
            src = mapping[obj_name]
            matrix.addVertex(src)
            if obj_name in function_roots:
                for k,v in self.schema.get_type(obj_name).fields.items():
                    dst = get_name(v.type)
                    dst = mapping.get(dst,False)
                    if dst != False:
                        matrix.addEdge(src,dst)
            else:
                for k,v in self.schema.get_type(obj_name).fields.items():
                    dst = get_name(v.type)
                    dst = mapping.get(dst,False)
                    if dst != False:
                        matrix.addEdge(src,dst)
        return trimmed,mapping,matrix
    def get_sensitive(self,pattern=DEFAULT_REGEX):
        def isInteresting(s):
            matches = re.findall(pattern, s, re.IGNORECASE)
            return bool(matches)
        poi = {
            "Interesting Functions Names": {},
            "Interesting Node Names": [],
            "Interesting Field Names": {},
        }
        mapping = list(self.schema.get_type_map().keys())
        mapping.remove(self.schema.get_query_type().name)
        mapping.remove(self.schema.get_mutation_type().name)
        poi["Interesting Functions Names"][self.schema.get_query_type().name] = [i for i in self.schema.get_query_type().fields.keys() if isInteresting(i)]
        poi["Interesting Functions Names"][self.schema.get_mutation_type().name] = [i for i in self.schema.get_mutation_type().fields.keys() if isInteresting(i)]
        poi["Interesting Node Names"] = [i for i in mapping if isInteresting(i)]
        for m in mapping:
            if isinstance(self.schema.get_type(m),graphql.type.definition.GraphQLObjectType):
                findings = [i for i in self.schema.get_type(m).fields.keys() if isInteresting(i)]
                if findings:
                    poi["Interesting Field Names"][m] = findings
        return poi

def remote_introspection(url,additional_headers=None):
    headers = {"Content-Type":"application/json"}
    headers.update(additional_headers if additional_headers else {})
    res = requests.post(url,headers=headers,json={"query":graphql.introspection_query})
    return res.json()

def load_remote_introspection(url,additional_headers=None):
    return load_introspection(remote_introspection(url,additional_headers)["data"])

def load_introspection(introspection):
    return graphql.build_client_schema(introspection)
