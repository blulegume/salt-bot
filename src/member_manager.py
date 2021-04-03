from json import load, dump
from member import Member
class MemberManager():
    '''
    A very simple data store
    '''
    _store = {}

    @classmethod
    def add_members(cls, guild_name, new_members):
        '''
        Add members to the member store for the specified guild (server)
        
        If the guild id is not already a key in the store, this method will add it
        '''
        if guild_name not in cls._store:
            cls._store[guild_name] = []

        guild_members = cls._store[guild_name]
        guild_member_ids = cls._get_member_ids(guild_members)
        for new_member in new_members:
            if new_member.id not in guild_member_ids:
                guild_members.append(Member(new_member.id, new_member.name, new_member.nick))
        cls._update_member_file()
        print(f'Added {", ".join(cls._get_member_names(new_members))}')

    @classmethod
    def remove_members(cls, guild_name, members):
        if guild_name not in cls._store:
            return
        else:
            guild_members = cls._store[guild_name]
            old_member_ids = list(map(lambda member: member.id, members))
            cls._store[guild_name] = list(filter(lambda member: member.id not in old_member_ids, guild_members))
        cls._update_member_file()
        print(f'Removed {", ".join(cls._get_member_names(members))}')

    @classmethod
    def clear_members(cls, guild_name):
        if guild_name not in cls._store:
            return
        cls._store[guild_name].clear()
        cls._update_member_file()
        print('Cleared member store')

    @classmethod
    def list_members(cls, guild_id):
        print(guild_id, cls._store[guild_id])
        if (not guild_id in cls._store) or (len(cls._store[guild_id]) == 0):
            return 'nobody!'
        return ', '.join(cls._get_member_nicks(cls._store[guild_id]))

    @classmethod
    def load_store(cls):
        with open('members.json', 'r') as f:
            store_dict = load(f)
            print(store_dict)
            cls._store = cls._map_members(store_dict, lambda member: Member(**member))
    
    @classmethod
    def exists(cls, guild_name, member_id):
        return guild_name in cls._store and member_id in cls._get_member_ids(cls._store[guild_name])

    @classmethod
    def _update_member_file(cls):
        with open('members.json', 'w') as f:
            store_dict = cls._map_members(cls._store, lambda member: member.as_dict)
            dump(store_dict, f)

    def _get_member_ids(members):
        return list(map(lambda member: member.id, members))

    def _get_member_names(members):
        return list(map(lambda member: member.name, members))

    def _get_member_nicks(members):
        return list(map(lambda member: member.nick, members))

    def _map_members(from_store, fn):
        to_store = {}
        for guild_name in from_store:
            to_store[guild_name] = list(map(fn, from_store[guild_name]))
        return to_store