using System.Collections.Generic;

namespace Identity.ViewModels.Token
{
    public interface IAccessToken
    {
        public IEnumerable<string> Roles { get; set; }
    }
}