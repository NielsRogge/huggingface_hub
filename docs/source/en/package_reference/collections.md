<!--⚠️ Note that this file is in Markdown but contains specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.
-->

# Managing collections

Check out the [`HfApi`] documentation page for the reference of methods to manage your Space on the Hub.

- Get collection content: [`get_collection`]
- Create new collection: [`create_collection`]
- Update a collection: [`update_collection_metadata`]
- Delete a collection: [`delete_collection`]
- Add an item to a collection: [`add_collection_item`]
- Update an item in a collection: [`update_collection_item`]
- Remove an item from a collection: [`delete_collection_item`]


### Collection

### Collection

```python
Contains information about a Collection on the Hub.

Attributes:
    slug (`str`):
        Slug of the collection. E.g. `"TheBloke/recent-models-64f9a55bb3115b4f513ec026"`.
    title (`str`):
        Title of the collection. E.g. `"Recent models"`.
    owner (`str`):
        Owner of the collection. E.g. `"TheBloke"`.
    items (`List[CollectionItem]`):
        List of items in the collection.
    last_updated (`datetime`):
        Date of the last update of the collection.
    position (`int`):
        Position of the collection in the list of collections of the owner.
    private (`bool`):
        Whether the collection is private or not.
    theme (`str`):
        Theme of the collection. E.g. `"green"`.
    upvotes (`int`):
        Number of upvotes of the collection.
    description (`str`, *optional*):
        Description of the collection, as plain text.
    url (`str`):
        (property) URL of the collection on the Hub.
```


### CollectionItem

### CollectionItem

```python
Contains information about an item of a Collection (model, dataset, Space or paper).

Attributes:
    item_object_id (`str`):
        Unique ID of the item in the collection.
    item_id (`str`):
        ID of the underlying object on the Hub. Can be either a repo_id or a paper id
        e.g. `"jbilcke-hf/ai-comic-factory"`, `"2307.09288"`.
    item_type (`str`):
        Type of the underlying object. Can be one of `"model"`, `"dataset"`, `"space"` or `"paper"`.
    position (`int`):
        Position of the item in the collection.
    note (`str`, *optional*):
        Note associated with the item, as plain text.
```

