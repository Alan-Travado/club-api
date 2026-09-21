from urllib.parse import urlencode

from flask import request


def armar_links(limit, offset, total):
    def link(nuevo_offset):
        params = request.args.to_dict()
        params["_limit"] = limit
        params["_offset"] = nuevo_offset
        return {"href": f"{request.base_url}?{urlencode(params)}"}

    ultimo = ((total - 1) // limit) * limit if total > 0 else 0

    links = {"_first": link(0)}
    if offset > 0:
        links["_prev"] = link(max(offset - limit, 0))
    if offset + limit < total:
        links["_next"] = link(offset + limit)
    links["_last"] = link(ultimo)
    return links
