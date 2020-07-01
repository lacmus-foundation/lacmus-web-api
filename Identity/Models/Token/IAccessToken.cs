using System.Collections.Generic;

namespace Identity.Models.Token
{
    public interface IAccessToken
    {
        public List<string> Roles { get; set; }
    }
}