<!--⚠️ Note that this file is in Markdown but contains specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.
-->

# 컬렉션 관리[[managing-collections]]

Hub에서 Space를 관리하는 메소드에 대한 자세한 설명은 [`HfApi`] 페이지를 확인하세요.

- 컬렉션 내용 가져오기: [`get_collection`]
- 새로운 컬렉션 생성: [`create_collection`]
- 컬렉션 업데이트: [`update_collection_metadata`]
- 컬렉션 삭제: [`delete_collection`]
- 컬렉션에 항목 추가: [`add_collection_item`]
- 컬렉션의 항목 업데이트: [`update_collection_item`]
- 컬렉션에서 항목 제거: [`delete_collection_item`]


### Collection[[huggingface_hub.Collection]]

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


### CollectionItem[[huggingface_hub.CollectionItem]]

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

