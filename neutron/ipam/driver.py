#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import abc

import six


@six.add_metaclass(abc.ABCMeta)
class Pool(object):
    """Interface definition for an IPAM driver.

    There should be an instance of the driver for every subnet pool.
    """

    def __init__(self, subnet_pool_id):
        """Initialize pool

        :param subnet_pool_id: SubnetPool ID of the address space to use.
        :type subnet_pool_id: str uuid
        """
        self._subnet_pool_id = subnet_pool_id

    @classmethod
    def get_instance(cls, subnet_pool_id):
        """Returns an instance of the configured IPAM driver

        :param subnet_pool_id: Subnet pool ID of the address space to use.
        :type subnet_pool_id: str uuid
        :returns: An instance of Driver for the given subnet pool
        """
        raise NotImplementedError

    @abc.abstractmethod
    def allocate_subnet(self, request):
        """Allocates a subnet based on the subnet request

        :param request: Describes the allocation requested.
        :type request: An instance of a sub-class of SubnetRequest
        :returns: An instance of Subnet
        :raises: RequestNotSupported, IPAMAlreadyAllocated
        """

    @abc.abstractmethod
    def get_subnet(self, subnet_id):
        """Gets the matching subnet if it has been allocated

        :param subnet_id: the subnet identifier
        :type subnet_id: str uuid
        :returns: An instance of IPAM Subnet
        :raises: IPAMAllocationNotFound
        """

    @abc.abstractmethod
    def update_subnet(self, request):
        """Updates an already allocated subnet

        This is used to notify the external IPAM system of updates to a subnet.

        :param request: Update the subnet to match this request
        :type request: An instance of a sub-class of SpecificSubnetRequest
        :returns: An instance of IPAM Subnet
        :raises: RequestNotSupported, IPAMAllocationNotFound
        """

    @abc.abstractmethod
    def remove_subnet(self, subnet_id):
        """Removes an allocation

        The initial reference implementation will probably do nothing.

        :param subnet_id: the subnet identifier
        :type subnet_id: str uuid
        :raises: IPAMAllocationNotFound
        """


@six.add_metaclass(abc.ABCMeta)
class Subnet(object):
    """Interface definition for an IPAM subnet

    A subnet would typically be associated with a network but may not be.  It
    could represent a dynamically routed IP address space in which case the
    normal network and broadcast addresses would be useable.  It should always
    be a routable block of addresses and representable in CIDR notation.
    """

    @abc.abstractmethod
    def allocate(self, address_request):
        """Allocates an IP address based on the request passed in

        :param address_request: Specifies what to allocate.
        :type address_request: An instance of a subclass of AddressRequest
        :returns: A netaddr.IPAddress
        :raises: AddressNotAvailable, AddressOutsideAllocationPool,
            AddressOutsideSubnet
        """

    @abc.abstractmethod
    def deallocate(self, address):
        """Returns a previously allocated address to the pool

        :param address: The address to give back.
        :type address: A netaddr.IPAddress or convertible to one.
        :returns: None
        :raises: IPAMAllocationNotFound
        """

    @abc.abstractmethod
    def get_details(self):
        """Returns the details of the subnet

        :returns: An instance of SpecificSubnetRequest with the subnet detail.
        """
